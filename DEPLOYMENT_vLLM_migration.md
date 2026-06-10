# Chakra AI — Ollama → vLLM Migration Runbook

**Goal:** fix the "slow / falls over past ~10 concurrent users" problem by replacing the
Ollama serving engine (no real concurrency) with **vLLM continuous batching**, keeping the
**same small model (Qwen3-4B)** and serving **hundreds** of concurrent chats.

Status: **PLAN ONLY** — nothing on the server has been changed (except a safety backup of the
app dir, see below). Steps marked 🔑 require **root** (the `llm2` account has no sudo).

---

## 0. Verified facts about the production box (`astra`, 14.195.197.108)

| Item | Value |
|---|---|
| OS / HW | Ubuntu 24.04, 2× **H100 NVL 96 GB**, 384 cores, 1 TB RAM |
| GPU 0 | ~26 GB free — already busy (llm1's gemma vLLM on `:5004`, others) |
| **GPU 1** | **~75 GB free** ← we deploy here |
| Chakra service | `chakra-backend.service` (systemd, **runs as root**), uvicorn `:8000` |
| Chakra code | `/home/llm2/rkm/backend` (owned by `llm2` — editable without root) |
| Chakra venv | `/home/llm2/rkm/backend/venv` (has `openai==2.41.0` already ✅) |
| Current models | Ollama `:11434` — `qwen3:4b` (text), `qwen2.5vl:7b` (vision) |
| Proven vLLM on box | `vllm 0.21.0 / torch 2.11+cu130` at `/opt/projects/qwen3-omni/env` (known-good) |
| Disk | `/` is **96% full (41 GB free)**; **`/data` = 24 TB, 2% used** (root-owned) |
| Free ports | 8001, 8002, 8003 |
| Safety backup made | `/home/llm2/rkm/backend/app.bak.20260610-231802` |

**Design decision:** text (95%+ of traffic) → **vLLM**. Image queries (rare) → **keep Ollama
`qwen2.5vl:7b`**. This gives the concurrency win on the hot path with zero risk to vision.

---

## 1. 🔑 Stand up the vLLM server (GPU 1)  — *root*

Put the model cache + (optionally) a dedicated venv on the big `/data` disk so `/` (96% full)
is never touched.

```bash
# as root
install -d -o llm2 -g llm2 /data/llm2/hf-cache          # model cache on the 24TB disk
```

### Option A (recommended, robust) — dedicated systemd service

Create `/etc/systemd/system/chakra-vllm.service`:

```ini
[Unit]
Description=vLLM Qwen3-4B (Chakra text model)
After=network-online.target
Wants=network-online.target

[Service]
User=llm2
Group=llm2
Environment=CUDA_VISIBLE_DEVICES=1
Environment=HF_HOME=/data/llm2/hf-cache
# Reuse the proven on-box vLLM. (Or install your own — see Option B.)
ExecStart=/opt/projects/qwen3-omni/env/bin/vllm serve Qwen/Qwen3-4B \
  --served-model-name qwen3-4b \
  --host 127.0.0.1 --port 8001 \
  --gpu-memory-utilization 0.40 \
  --max-model-len 8192 \
  --max-num-seqs 256
Restart=always
RestartSec=10
TimeoutStartSec=600

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable --now chakra-vllm.service
journalctl -u chakra-vllm -f          # watch first-time model download (~8 GB) + load
```

- `--gpu-memory-utilization 0.40` ≈ 38 GB on GPU 1 (fits inside the 75 GB free) → 4B weights
  (~8 GB) + large KV cache → easily **256 concurrent sequences**.
- `--max-num-seqs 256` is the batch width — the lever that fixes the >10-user wall.

### Option B (fully isolated, no dependency on llm1's env)

```bash
install -d -o llm2 -g llm2 /data/llm2/vllm-chakra
sudo -u llm2 python3 -m venv /data/llm2/vllm-chakra/env
sudo -u llm2 /data/llm2/vllm-chakra/env/bin/pip install "vllm==0.21.0"
# then point ExecStart at /data/llm2/vllm-chakra/env/bin/vllm
```

### Verify the server in isolation (any user) — **before** touching Chakra
```bash
curl -s http://127.0.0.1:8001/v1/models | python3 -m json.tool
curl -s http://127.0.0.1:8001/v1/chat/completions -H 'Content-Type: application/json' -d '{
  "model":"qwen3-4b",
  "messages":[{"role":"user","content":"Say hello in one sentence."}],
  "max_tokens":50, "stream":false
}'
```
Only proceed once this returns a completion.

---

## 2. Edit Chakra code (no root needed — `llm2` owns these files)

### 2a. `app/core/config.py` — add vLLM settings (keep the Ollama ones for vision/fallback)

```python
    # LLM Models
    EMBED_MODEL_NAME: str = "text-embedding-3-small"
    OLLAMA_TEXT_MODEL: str = "qwen3:4b"          # kept as fallback
    OLLAMA_VISION_MODEL: str = "qwen2.5vl:7b"    # vision path stays on Ollama

    # vLLM (primary text engine — OpenAI-compatible, local)
    VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL", "http://127.0.0.1:8001/v1")
    VLLM_TEXT_MODEL: str = os.getenv("VLLM_TEXT_MODEL", "qwen3-4b")
    VLLM_MAX_TOKENS: int = int(os.getenv("VLLM_MAX_TOKENS", "1200"))
```

### 2b. `app/services/llm_service.py` — replace the streaming engine

Replace the body of `generate_response_stream(...)` so **text streams from vLLM** and **images
still use Ollama**. The NDJSON contract (`{"token": ...}`, refs, `suggested_questions`,
`addl_ai`) is unchanged, so **the frontend needs no changes**.

Key differences vs. today:
- `num_predict: -1` (unlimited) → **`max_tokens = settings.VLLM_MAX_TOKENS`** (caps verbose
  answers so one user can't hog the batch).
- Qwen3 "thinking" disabled for chat latency via
  `extra_body={"chat_template_kwargs": {"enable_thinking": False}}`.
- The per-request `ThreadPoolExecutor(max_workers=100)` should be a single module-level pool
  (see note in §4).

```python
# at top of file
from openai import OpenAI
# module-level reusable client to the local vLLM server
_vllm_client = OpenAI(base_url=settings.VLLM_BASE_URL, api_key="not-needed")

# ... inside generate_response_stream(...), replace the Ollama streaming block:

    full_content = ""
    try:
        if image_bytes:
            # RARE path: vision stays on Ollama (qwen2.5vl)
            import ollama
            msg = {'role': 'user', 'content': final_prompt, 'images': [image_bytes]}
            stream = ollama.chat(
                model=settings.OLLAMA_VISION_MODEL, messages=[msg], stream=True,
                options={"temperature": 0.8, "top_p": 0.9, "num_ctx": 4096, "num_gpu": 99},
            )
            for chunk in stream:
                content = chunk["message"]["content"]
                full_content += content
                yield json.dumps({"token": content}) + "\n"
        else:
            # HOT path: text via vLLM continuous batching
            stream = _vllm_client.chat.completions.create(
                model=settings.VLLM_TEXT_MODEL,
                messages=[{"role": "user", "content": final_prompt}],
                temperature=0.8, top_p=0.9,
                max_tokens=settings.VLLM_MAX_TOKENS,
                stream=True,
                extra_body={"chat_template_kwargs": {"enable_thinking": False}},
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    full_content += delta
                    yield json.dumps({"token": delta}) + "\n"
    except Exception as e:
        print(f"[Chat] Primary (vLLM/Ollama) streaming failed: {e}")
        yield json.dumps({"token": "The notes engine is currently busy. Please retry."}) + "\n"

    # ... the rest (reference chunks, suggested-questions regex, gpt-4o-mini addl_ai) is UNCHANGED
```

> The existing `gpt-4o-mini` "additional AI" path and the references / suggested-questions
> parsing stay exactly as they are.

---

## 3. 🔑 Cut over — *root* (loads the edited code)

```bash
systemctl restart chakra-backend.service
systemctl status chakra-backend.service --no-pager
journalctl -u chakra-backend -n 50 --no-pager
```

Smoke test through the real API (text path → should now be vLLM):
```bash
curl -s -X POST http://127.0.0.1:8000/api/chat -F 'query=Explain depreciation briefly' | head
```

---

## 4. Recommended cleanups (do with the edit in §2)

- **Shared threadpool:** move `concurrent.futures.ThreadPoolExecutor(max_workers=100)` out of
  `generate_response_stream` to a single module-level pool (e.g. `max_workers=32`). Today a new
  100-thread pool is created on *every* chat request.
- **uvicorn workers (🔑 service file):** add `--workers 4` to the `ExecStart` in
  `chakra-backend.service` so the HTTP layer isn't a single process. (vLLM handles GPU fan-out;
  workers handle HTTP fan-out.)
- Optional: cache OpenAI embeddings for repeated queries to shave a network round-trip.

---

## 5. Capacity expectation

| | Before (Ollama) | After (vLLM, GPU 1 only) |
|---|---|---|
| Concurrent chats before queueing | ~2–4 | ~**100–300+** |
| GPU utilization under load | ~1–2% | high (batched) |
| Model / answer quality | Qwen3-4B | Qwen3-4B (same) |
| Frontend changes | — | none |

Need even more headroom later: run a 2nd vLLM replica and round-robin, or move to a larger
model across both GPUs (tensor-parallel) — both are drop-in from here.

---

## 6. Rollback (instant, low-risk)

The code keeps Ollama for vision and the change is contained to `generate_response_stream`.

```bash
# revert code
rm -rf /home/llm2/rkm/backend/app
mv /home/llm2/rkm/backend/app.bak.20260610-231802 /home/llm2/rkm/backend/app
# 🔑 root:
systemctl restart chakra-backend.service
systemctl stop chakra-vllm.service     # optional: free GPU 1
```

(If you only changed the two files, restoring `config.py` + `llm_service.py` from the backup is
enough — no need to swap the whole dir.)
```
