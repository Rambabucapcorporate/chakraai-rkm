# app/api/routers/chat.py
#
# =====================================================================
# PRESERVED CHAT ENDPOINTS — The embedding logic is untouched.
# Only the routing layer has been reorganized.
# =====================================================================

from fastapi import APIRouter, BackgroundTasks, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from starlette.concurrency import run_in_threadpool
from typing import Optional
import json
import os
from app.core.config import settings
from app.schemas.chat import LoadRequest, SubjectSelectionRequest
from app.services.llm_service import (
    load_subject_files,
    query_knowledge_base,
    build_prompt,
    generate_response_stream,
)

# Import configure functions (configure.py remains at backend root)
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from configure import get_subject_files, get_source_filters
from app.services.audit import user_from_auth_header, save_chat_log, log_activity, save_feedback

router = APIRouter(prefix="/api", tags=["Chat & Knowledge Base"])


def _logged_stream(inner, user_id, username, question, model, endpoint):
    """Pass a chat NDJSON stream through, accumulate the answer tokens, then log the Q&A + latency."""
    import time
    parts = []
    _t0 = time.time()
    for chunk in inner:
        try:
            d = json.loads(chunk)
            if d.get("token"):
                parts.append(d["token"])
        except Exception:
            pass
        yield chunk
    _latency_ms = int((time.time() - _t0) * 1000)
    _cid = save_chat_log(user_id, username, question, "".join(parts), model, endpoint, _latency_ms)
    log_activity(user_id, username, "chat", question)
    if _cid:
        # tell the client which row this answer is, so it can attach 👍/👎 feedback
        yield json.dumps({"chat_id": _cid}) + "\n"


@router.post("/feedback")
async def feedback(request: Request, chat_id: int = Form(...), rating: int = Form(...)):
    """Record a thumbs up (1) / down (-1) / clear (0) rating on an answer, for RL / quality review."""
    if rating not in (1, -1, 0):
        raise HTTPException(status_code=400, detail="rating must be 1, -1, or 0")
    _uid, _uname = user_from_auth_header(request.headers.get("Authorization", ""))
    ok = save_feedback(chat_id, rating, _uid)
    return {"ok": ok}


@router.get("/files")
async def list_files():
    """List all available JSON embedding files across all knowledge base directories."""
    all_files = []
    # Relevant data directory prefixes
    data_prefixes = ["No_images_data", "processed_data", "knowledge_base"]
    
    # Walk through the current directory (backend root)
    for root, _, files in os.walk("."):
        # Skip internal system directories for performance
        if any(skip in root for skip in ["venv", "__pycache__", "chroma_db", ".git", "app", "configs"]):
            continue
            
        for f in files:
            if f.endswith(".json"):
                # Get path relative to the backend root
                rel_path = os.path.relpath(os.path.join(root, f), ".").replace("\\", "/")
                
                # Only include if it lives within one of our target knowledge base folders
                if any(rel_path.startswith(prefix) for prefix in data_prefixes):
                    all_files.append(rel_path)
                    
    return {"files": sorted(all_files)}


@router.post("/load")
async def load_knowledge_base(request: LoadRequest, background_tasks: BackgroundTasks):
    """
    Load knowledge base files. Expects request.filenames to be a list of book dictionaries:
    [{"title": "Book Title", "file": "path/to/file.json"}, ...]
    """
    book_list = []
    for item in request.filenames:
        if isinstance(item, dict):
            book_list.append(item)
        else:
            book_list.append({"title": item, "file": item})
    
    background_tasks.add_task(load_subject_files, book_list)
    return {
        "status": "loading_started", 
        "message": f"Loading {len(book_list)} files in background"
    }


@router.post("/set_subject")
async def set_subject(request: SubjectSelectionRequest, background_tasks: BackgroundTasks):
    """
    Sets the current subject and triggers data loading for that subject.
    """
    print(f"[Set Subject] Received request: {request}")
    
    book_list = get_subject_files(
        year=request.year,
        branch=request.branch,
        semester=request.semester,
        subject=request.subject
    )
    
    if not book_list:
        return {
            "status": "warning",
            "message": f"No books found for subject: {request.subject}"
        }

    loaded_books = load_subject_files(book_list)
    
    return {
        "status": "success",
        "message": f"Loaded {len(loaded_books)} books for {request.subject}",
        "books": loaded_books
    }


@router.post("/chat")
async def chat(
    request: Request,
    query: str = Form(...),
    history: str = Form("[]"),
    subject: Optional[str] = Form(None),
    year: Optional[str] = Form(None),
    branch: Optional[str] = Form(None),
    semester: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    """
    Main chat endpoint — subject-scoped RAG (dense retrieval + cross-encoder rerank), strict grounding.

    Text queries retrieve from ONLY the selected subject's books, cite the pages used, and refuse
    when the answer isn't in those books. Image queries answer via the vision model directly (no RAG).
    Preserves the existing contract: streaming, suggested questions, and the OpenAI "Additional AI" panel.
    """
    prompt = query
    image_bytes = await image.read() if image else None
    _uid, _uname = user_from_auth_header(request.headers.get("Authorization", ""))
    _model = settings.OLLAMA_VISION_MODEL if image_bytes else settings.VLLM_MODEL

    # --- Image path: vision model answers directly (RAG is text-only) ---
    if image_bytes:
        final_prompt = (
            "You are an academic assistant for Ramakrishna Mission Vivekananda College. "
            "Answer the student's question clearly, accurately, and in depth using Markdown "
            "(headers, **bold** key terms, bullet points, tables where useful).\n\n"
            f"Question: {prompt}\n"
        )
        return StreamingResponse(
            _logged_stream(
                # raw_query=None → no OpenAI "Additional AI" side panel
                generate_response_stream(final_prompt, image_bytes, [], raw_query=None, subject=subject),
                _uid, _uname, query, _model, "chat",
            ),
            media_type="application/x-ndjson",
        )

    # --- Text path: subject-scoped dense + rerank RAG with 3-step progress ---
    def gen():
        import time
        yield json.dumps({"status": "Step 1 of 3) Understanding your question"}) + "\n"
        time.sleep(0.3)
        yield json.dumps({"status": "Step 2 of 3) Retrieving relevant sections"}) + "\n"

        context = ""
        citations = []
        try:
            docs, metas, _sources = _subject_dense_candidates(query, year, branch, semester, subject, RAG_FETCH_K)
            docs, metas = _rerank(query, docs, metas, settings.RAG_N_RESULTS)
            parts = []
            seen = set()
            for d, m in zip(docs, metas):
                src = m.get("source", "?")
                pg = m.get("page", "?")
                parts.append(f"Source: {src}, Page: {pg}\nContent: {d}")
                key = (src, pg)
                if key not in seen:
                    seen.add(key)
                    citations.append({
                        "source": src,
                        "page": pg,
                        "text": f"{src}, p.{pg}",
                        "pdf": bool(_pdf_path_for(src)),
                    })
            context = "\n\n---\n\n".join(parts)
        except Exception as e:
            print(f"[chat] retrieval failed: {e}")

        yield json.dumps({"status": "Step 3 of 3) Answering"}) + "\n"
        time.sleep(0.2)

        # Strict, explicit-refusal prompt (build_prompt's soft instruction let qwen answer
        # out-of-scope questions from general knowledge). Keeps inline citations + Explore Further.
        final_prompt = (
            "You are an academic assistant for Ramakrishna Mission Vivekananda College.\n"
            "Answer the student's question using ONLY the Context below, taken from the student's "
            "course materials. Each Context passage is labelled with its Source filename and Page number.\n\n"
            "STRICT RULES:\n"
            "1. Use ONLY the Context. Do NOT use outside or general knowledge. Do NOT guess.\n"
            "2. If the answer is not contained in the Context, reply with EXACTLY this sentence and "
            "nothing else: I don't have that information in your course materials.\n"
            "3. When you do answer, cite the exact Source filename and Page for each claim, inline, "
            "as [Source: filename, Page: X].\n"
            "4. Format with Markdown: headers (##, ###), **bold** key terms, bullet points, and tables where useful.\n"
            "5. Do NOT output chain-of-thought or any thinking tags.\n\n"
            "After a real answer ONLY (never after a refusal), add a section titled exactly "
            "'🧐 Explore Further:' with 3-4 short follow-up questions. Each question MUST be "
            "answerable from the Context above — only ask about topics, terms, and examples that "
            "actually appear in the Context. Do NOT ask about concepts that are not present in the "
            "Context. Put each on its own line starting with '- ' and ending with '?'.\n\n"
            f"Context:\n{context}\n\nQuestion: {query}\n"
        )

        answer_parts = []
        try:
            # raw_query=None → no OpenAI "Additional AI" side panel (suggested_questions still emitted)
            for chunk in generate_response_stream(final_prompt, None, [], raw_query=None, subject=subject):
                try:
                    _d = json.loads(chunk)
                    if _d.get("token"):
                        answer_parts.append(_d["token"])
                except Exception:
                    pass
                yield chunk
        except Exception as e:
            print(f"[chat] generation failed: {e}")
            yield json.dumps({"token": "Sorry, the answer engine is busy. Please retry."}) + "\n"

        # Only surface citations when the answer is grounded (strip the auto-appended sections first).
        answer_main = _re.split(r"🧐 Explore Further:|### 📚 Reference Chunks", "".join(answer_parts))[0]
        if citations and _answer_is_grounded(answer_main):
            yield json.dumps({"citations": citations}) + "\n"

    return StreamingResponse(
        _logged_stream(gen(), _uid, _uname, query, _model, "chat"),
        media_type="application/x-ndjson",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )


# =====================================================================
# SIMPLE ONE-BOOK RAG (demo) — 3-step progress + retrieval from a single book
# Reuses the existing ChromaDB collection (OpenAI embeddings) and vLLM streamer.
# The live /api/chat above is untouched.
# =====================================================================
from app.services.llm_service import collection as _rag_collection, _stream_vllm as _rag_stream_vllm
from urllib.request import Request as _RRReq, urlopen as _rropen

RAG_BOOK = "Financial Accounting For Management (Ramachandran And K Ramkumar) (Z-Library).pdf"
RAG_BOOK_PDF = "/home/llm2/rag/rkmbooks/Accounting for managers/Financial Accounting For Management (Ramachandran And K Ramkumar) (Z-Library).pdf"
RAG_TOP_K = 6            # chunks fed to the LLM
RAG_FETCH_K = 20        # wider dense candidate set for the re-ranker
RERANK_URL = "http://127.0.0.1:8002/rerank"

# On-disk book PDFs, used to deep-link citations to #page=N. Only books whose PDF is present
# here get clickable citations; everything else falls back to plain source+page text.
RKMBOOKS_DIR = "/home/llm2/rag/rkmbooks"
_pdf_index = None


def _pdf_path_for(source):
    """Resolve a book 'source' filename to its on-disk PDF path (cached). None if not present."""
    global _pdf_index
    if _pdf_index is None:
        _pdf_index = {}
        try:
            for root, _dirs, files in os.walk(RKMBOOKS_DIR):
                for f in files:
                    if f.lower().endswith(".pdf"):
                        _pdf_index.setdefault(f, os.path.join(root, f))
        except Exception as e:
            print(f"[chat] pdf index build failed: {e}")
    return _pdf_index.get(source) if source else None


@router.get("/book_pdf")
def book_pdf(source: Optional[str] = None):
    """Serve a book PDF inline for citation deep-links (#page=N).

    `source` selects the book by its metadata filename; omitted → the demo book (back-compat).
    Returns 404 when the requested book has no PDF on disk.
    """
    path = RAG_BOOK_PDF
    if source:
        resolved = _pdf_path_for(source)
        if not resolved:
            raise HTTPException(status_code=404, detail="No PDF available for this source")
        path = resolved
    return FileResponse(path, media_type="application/pdf", headers={"Content-Disposition": "inline"})


def _rerank(query, docs, metas, top_k):
    """Cross-encoder rerank the dense candidates; fall back to dense top-k if the reranker is unavailable."""
    if not docs:
        return docs, metas
    try:
        body = json.dumps({"query": query, "documents": docs, "top_k": top_k}).encode()
        req = _RRReq(RERANK_URL, data=body, headers={"Content-Type": "application/json"})
        with _rropen(req, timeout=8) as r:
            results = json.loads(r.read()).get("results", [])
        order = [x["index"] for x in results if 0 <= x["index"] < len(docs)]
        if not order:
            return docs[:top_k], metas[:top_k]
        return [docs[i] for i in order], [metas[i] for i in order]
    except Exception as e:
        print(f"[chat_rag] rerank unavailable, using dense top-k: {e}")
        return docs[:top_k], metas[:top_k]


# ---- Sparse (BM25) index over the one book's chunks, built lazily + cached ----
import re as _re

_bm25 = None
_bm25_docs = None
_bm25_metas = None


def _tok(s):
    return _re.findall(r"[a-z0-9]+", (s or "").lower())


def _get_bm25():
    global _bm25, _bm25_docs, _bm25_metas
    if _bm25 is None:
        from rank_bm25 import BM25Okapi
        got = _rag_collection.get(where={"source": RAG_BOOK}, include=["documents", "metadatas"])
        _bm25_docs = got["documents"]
        _bm25_metas = got["metadatas"]
        _bm25 = BM25Okapi([_tok(d) for d in _bm25_docs])
    return _bm25


def _hybrid_candidates(query, k):
    """Union of dense (Chroma) top-k + sparse (BM25) top-k, deduped. Falls back to dense-only on BM25 error."""
    dr = _rag_collection.query(query_texts=[query], n_results=k, where={"source": RAG_BOOK})
    docs = list((dr.get("documents") or [[]])[0])
    metas = list((dr.get("metadatas") or [[]])[0])
    try:
        bm = _get_bm25()
        scores = bm.get_scores(_tok(query))
        order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        seen = set(docs)
        for i in order:
            d = _bm25_docs[i]
            if d not in seen:
                seen.add(d)
                docs.append(d)
                metas.append(_bm25_metas[i])
    except Exception as e:
        print(f"[chat_rag] BM25 unavailable, dense-only: {e}")
    return docs, metas


# The retriever always returns its top-k chunks, even for out-of-scope questions. When the
# model answers "not in this book", those chunks weren't used — so we must NOT cite them.
# These markers match the canonical refusal plus the common paraphrases the model emits.
_REFUSAL_MARKERS = (
    "don't have that information",
    "do not have that information",
    "not mentioned in the provided context",
    "not in the provided context",
    "not contained in the context",
    "not available in the provided",
    "cannot provide details",
    "can't provide details",
    "no mention of",
    "not in this book",
    "isn't in this book",
    "is not in this book",
    "not found in the",
    # build_prompt (main /api/chat) refusal phrasing
    "unavailable in the given context",
    "information is unavailable",
    "not contain sufficient information",
    "does not contain sufficient information",
    "insufficient information in the",
    "i am an academic assistant and can only answer",
)


def _answer_is_grounded(answer: str) -> bool:
    """True only if the answer actually drew on the retrieved context (i.e. is not a 'not found' reply)."""
    a = (answer or "").strip().lower()
    if not a:
        return False
    return not any(m in a for m in _REFUSAL_MARKERS)


def _subject_dense_candidates(query, year, branch, semester, subject, fetch_k):
    """Dense retrieval scoped to the selected subject's books only (via get_source_filters).

    Returns (docs, metas, sources). Empty when the subject maps to no books — which, under the
    strict prompt, makes the model reply that the answer isn't in the course materials.
    """
    try:
        sources = get_source_filters(year, branch, semester, subject, base_directory=".")
    except Exception as e:
        print(f"[chat] get_source_filters failed: {e}")
        sources = []
    if not sources:
        return [], [], []
    where = {"source": sources[0]} if len(sources) == 1 else {"source": {"$in": sources}}
    r = _rag_collection.query(query_texts=[query], n_results=fetch_k, where=where)
    docs = list((r.get("documents") or [[]])[0])
    metas = list((r.get("metadatas") or [[]])[0])
    return docs, metas, sources


@router.post("/chat_rag")
async def chat_rag(request: Request, query: str = Form(...), history: str = Form("[]")):
    """One-book RAG with 3-step progress. Retrieves from RAG_BOOK (OpenAI embeddings), answers via vLLM."""

    def gen():
        import time
        yield json.dumps({"status": "Step 1 of 3) Understanding your question"}) + "\n"
        time.sleep(0.5)
        yield json.dumps({"status": "Step 2 of 3) Retrieving relevant sections"}) + "\n"

        context = ""
        citations = []
        try:
            # hybrid retrieval: dense (Chroma) ∪ sparse (BM25), then cross-encoder rerank to top-k
            docs, metas = _hybrid_candidates(query, RAG_FETCH_K)
            docs, metas = _rerank(query, docs, metas, RAG_TOP_K)
            parts = []
            for d, m in zip(docs, metas):
                src = m.get("source", "?")
                pg = m.get("page", "?")
                parts.append(f"[{src} p.{pg}]\n{d}")
                cite = f"{src}, p.{pg}"
                if cite not in citations:
                    citations.append(cite)
            context = "\n\n".join(parts)
        except Exception as e:
            print(f"[chat_rag] retrieval failed: {e}")

        yield json.dumps({"status": "Step 3 of 3) Answering"}) + "\n"
        time.sleep(0.4)

        prompt = (
            "You are an academic assistant for Ramakrishna Mission Vivekananda College. "
            f"Answer the student's question using ONLY the Context below, taken from the book '{RAG_BOOK}'. "
            "Cite sources inline as [source, page]. If the answer is not contained in the Context, reply "
            "with exactly this sentence and nothing else: I don't have that information in this book. "
            "Use Markdown: headers (##, ###), **bold** key terms, bullet points, and tables where useful.\n\n"
            f"Context:\n{context}\n\nQuestion: {query}\n"
        )

        holder = [""]
        answer_parts = []
        try:
            for chunk in _rag_stream_vllm(prompt, holder):
                # accumulate the answer text so we can tell whether it used the retrieved context
                try:
                    _d = json.loads(chunk)
                    if _d.get("token"):
                        answer_parts.append(_d["token"])
                except Exception:
                    pass
                yield chunk
        except Exception as e:
            print(f"[chat_rag] generation failed: {e}")
            yield json.dumps({"token": "Sorry, the answer engine is busy. Please retry."}) + "\n"

        # Only surface citations when the answer is actually grounded in the retrieved pages.
        answer_text = "".join(answer_parts) or holder[0]
        if citations and _answer_is_grounded(answer_text):
            yield json.dumps({"citations": citations}) + "\n"

    _uid, _uname = user_from_auth_header(request.headers.get("Authorization", ""))
    return StreamingResponse(
        _logged_stream(gen(), _uid, _uname, query, "qwen3-4b (RAG)", "chat_rag"),
        media_type="application/x-ndjson",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )
