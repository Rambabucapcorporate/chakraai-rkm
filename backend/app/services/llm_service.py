# app/services/llm_service.py
#
# =====================================================================
# THIS FILE CONTAINS THE PRESERVED EMBEDDING AND LLM LOGIC.
# The internal algorithms, prompts, and ChromaDB interactions have
# NOT been modified — they were lifted directly from the original main.py.
# =====================================================================

import os
import json
import re
import chromadb
from chromadb.utils.embedding_functions import EmbeddingFunction
from chromadb import Documents, Embeddings
from openai import OpenAI
import ollama
from app.core.config import settings

# Import the configuration logic (configure.py remains at backend root)
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from configure import resolve_files, get_source_filters, get_subject_files


# ================== CUSTOM OPENAI EMBEDDING CLASS ==================
class OpenAIEmbeddingFunction(EmbeddingFunction):
    def __init__(self, api_key: str, model_name: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def __call__(self, input: Documents) -> Embeddings:
        response = self.client.embeddings.create(
            model=self.model_name,
            input=input
        )
        return [e.embedding for e in response.data]


# ================== CHROMADB SETUP ==================
openai_ef = OpenAIEmbeddingFunction(
    api_key=settings.OPENAI_API_KEY,
    model_name=settings.EMBED_MODEL_NAME
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name="multimodal_rag_final_1536",
    embedding_function=openai_ef
)


# ================== vLLM CLIENT (primary text engine) ==================
# Reusable client to the local vLLM server (OpenAI-compatible API).
# vLLM does PagedAttention + continuous batching, so many concurrent chats
# share the GPU instead of queueing the way Ollama does.
_vllm_client = OpenAI(base_url=settings.VLLM_BASE_URL, api_key="not-needed")


# ================== HELPER FUNCTIONS ==================

def load_subject_files(book_list):
    """
    Loads all available book files for a subject into ChromaDB.
    Expects JSON files with pre-computed embeddings in format:
    [{"id": "...", "embedding": [...], "document": "...", "metadata": {...}}, ...]
    """
    loaded_books = []
    
    for book in book_list:
        file_path = os.path.join(settings.EMBEDDINGS_DIRECTORY, book['file'])
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                # Check if data has pre-computed embeddings
                if isinstance(data, list) and len(data) > 0 and "id" in data[0]:
                    ids = [item['id'] for item in data]
                    embeddings = [item['embedding'] for item in data]
                    documents = [item['document'] for item in data]
                    metadatas = [item['metadata'] for item in data]
                    
                    # Batch upsert for efficiency
                    batch_size = 500
                    total = len(ids)
                    
                    for j in range(0, total, batch_size):
                        collection.upsert(
                            ids=ids[j:j+batch_size],
                            embeddings=embeddings[j:j+batch_size],
                            documents=documents[j:j+batch_size],
                            metadatas=metadatas[j:j+batch_size]
                        )
                    loaded_books.append(book['title'])
                    print(f"[Load] Loaded {book['title']} ({len(ids)} chunks)")
            except Exception as e:
                print(f"[Load] Error loading {book['title']}: {e}")
    
    return loaded_books


def query_knowledge_base(prompt, year, branch, semester, subject):
    """
    Queries ChromaDB with source filters based on the subject selection.
    Returns (context_string, retrieved_chunks_info_list).
    """
    source_filters = get_source_filters(
        year=year,
        branch=branch,
        semester=semester,
        subject=subject,
        base_directory="."
    )
    
    print(f"[Chat] Querying sources: {source_filters}")

    results = None
    if source_filters:
        if len(source_filters) == 1:
            where_filter = {"source": source_filters[0]}
        else:
            where_filter = {"source": {"$in": source_filters}}
            
        results = collection.query(
            query_texts=[prompt], 
            n_results=12,
            where=where_filter 
        )
    else:
        print("[Chat] No source filters found, trying broad search...")
        results = collection.query(
            query_texts=[prompt], 
            n_results=12
        )
    
    context = ""
    retrieved_chunks_info = []

    if results["documents"] and results["documents"][0]:
        context_parts = []
        for i, doc in enumerate(results["documents"][0]):
            source_meta = "Unknown Source"
            page_meta = "Unknown Page"
            if results["metadatas"] and len(results["metadatas"]) > 0:
                meta = results["metadatas"][0][i]
                source_meta = meta.get("source", "Unknown Source")
                page_meta = meta.get("page", "Unknown Page")
            
            context_parts.append(f"Source: {source_meta}, Page: {page_meta}\nContent: {doc}")
            retrieved_chunks_info.append(f"**Source:** {source_meta}\n**Page:** {page_meta}\n\n**Content:** {doc}")
        
        context = "\n\n---\n\n".join(context_parts)
    
    return context, retrieved_chunks_info


def build_prompt(context, prompt):
    """Builds the full augmented prompt for the LLM."""
    instruction_prefix = """
You are an advanced academic assistant for Ramakrishna Mission Vivekananda College.
Your goal is to provide COMPREHENSIVE and DETAILED academic responses.
While the provided Context is your primary source of truth, you should use your intelligence to 
thoroughly explain, define, and elaborate on the concepts mentioned. 
Do not just list facts; provide a rich, educational synthesis of the information.
"""

    final_prompt = f"""
{instruction_prefix}

Each piece of textual Context is labeled with its Source filename and Page number.

If the provided Context and Image do NOT contain sufficient information to answer the Question:
- Do NOT infer
- Do NOT use general or external knowledge
- Do NOT guess

Instead, clearly state that the information is unavailable in the given context.

Mandatory Citation Rule:
- You MUST cite the specific Source filename and Page number(s) used for your answer.
- Format citations as [Source: filename, Page: X] at the end of the relevant sentence or section.

Context:
{context}

Question:
{prompt}

IMPORTANT RULES:
1. Use Markdown headers (##, ###)
2. Use tables where applicable
3. Use bullet points for lists
4. Bold key academic terms
5. Maintain formal academic tone
6. NEVER answer outside the Context or Image
7. ALWAYS include citations with page numbers for text sources
8. If the answer comes from the Image, mention "Based on the image..."

MANDATORY SECTION:
Add a section titled "🧐 Explore Further:" ONLY if the question was answered using Context/Image.
In this section, provide 3-4 specific, thought-provoking questions that the user can ask to dive deeper into the topic.

FORMATTING RULES FOR BUTTONS:
- Each question MUST be on its own line.
- Start each line with a simple dash "- " or a number "1. ".
- Do NOT use bolding (**) or other special formatting inside the question text.
- Each line must end with a question mark "?".
"""
    return final_prompt


import concurrent.futures

def generate_response_stream(final_prompt, image_bytes, retrieved_chunks_info, raw_query=None, subject=None):
    """
    Generator that streams LLM responses from Ollama.
    Yields NDJSON chunks.
    """
    gen_options = {
        "num_predict": -1, 
        "temperature": 0.8, 
        "top_p": 0.9,
        "num_ctx": 4096,
    }

    # Start OpenAI query in a background thread if raw_query is provided
    openai_future = None
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def fetch_openai_response(q):
        if not settings.OPENAI_API_KEY:
            return "OpenAI API key is not configured."
        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            subject_str = f" specializing in {subject}" if subject else ""
            system_instruction = (
                f"You are an expert academic tutor and subject matter specialist{subject_str}. "
                "Students will ask questions, and your goal is to provide a comprehensive, "
                "highly detailed, and structured explanation of the relevant educational concepts. "
                "CRITICAL RULE: You must ONLY answer academic, educational, or subject-specific questions. "
                "If a question is clearly irrelevant to academics, study help, or college-level learning (such as general conversation, social chit-chat, jokes, weather, entertainment, non-academic tasks, or personal questions), "
                "you MUST refuse to answer. In case of refusal, respond exactly with: 'I am an academic assistant and can only answer academic or educational queries.' "
                "and do not provide any other explanation, text, or signature.\n\n"
                "IMPORTANT EXCEPTION: If the user asks for a broad topic or uses vague phrasing like 'give me the financial accounting', 'tell me about X', or 'explain Y', you MUST treat it as a valid academic request to explain that topic comprehensively.\n\n"
                "Adhere to the following guidelines for academic queries:\n"
                "1. Focus strictly on academic and educational topics.\n"
                "2. Provide in-depth explanations, defining terms clearly and breaking down complex ideas step-by-step.\n"
                "3. Include relevant illustrative examples, code/text snippets (using syntax highlighting blocks), diagrams, or equations where applicable.\n"
                "4. Structure your response using markdown headers (###), bullet points, and bold text for key academic terminology.\n"
                "5. Maintain a supportive, formal, and educational tone suitable for college-level learning."
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": q}
                ]
            )
            ans = response.choices[0].message.content
            
            # If the response is a refusal, return it directly without the signature
            if "can only answer academic or educational queries" in ans:
                return ans.strip()

            # Append college name signature
            sig = "Source documents from RKM Vivekananda College"
            if not ans.strip().endswith(sig):
                ans = ans.strip() + f"\n\n{sig}"
            return ans
        except Exception as e:
            return f"Error querying OpenAI: {str(e)}"

    if raw_query:
        openai_future = executor.submit(fetch_openai_response, raw_query)

    full_content = ""

    try:
        if image_bytes:
            # ---- RARE path: vision queries stay on Ollama (qwen2.5vl) ----
            target_model = settings.OLLAMA_VISION_MODEL
            print(f"[Chat] Image detected, using vision model: {target_model}")
            message = {'role': 'user', 'content': final_prompt, 'images': [image_bytes]}
            stream = ollama.chat(
                model=target_model,
                messages=[message],
                stream=True,
                options=gen_options,
            )
            for chunk in stream:
                content = chunk["message"]["content"]
                full_content += content
                yield json.dumps({"token": content}) + "\n"
        else:
            # ---- HOT path: text queries via local vLLM (continuous batching) ----
            # OpenAI-compatible streaming. max_tokens caps verbose answers so one
            # request can't monopolise the batch. enable_thinking=False keeps
            # Qwen3 from emitting reasoning tokens, cutting chat latency.
            stream = _vllm_client.chat.completions.create(
                model=settings.VLLM_TEXT_MODEL,
                messages=[{"role": "user", "content": final_prompt}],
                temperature=0.8,
                top_p=0.9,
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
        print(f"[Chat] Primary LLM streaming failed: {e}")
        # Yield a clear fallback token so the UI knows the engine failed
        fallback_msg = "I couldn't find any relevant information in the uploaded notes for that query (Primary AI/notes engine is currently busy or unavailable)."
        yield json.dumps({"token": fallback_msg}) + "\n"

    # Append Reference Chunks
    if retrieved_chunks_info:
        ref_text = "\n\n---\n\n### 📚 Reference Chunks\n"
        for i, chunk_info in enumerate(retrieved_chunks_info):
            ref_text += f"**Chunk {i+1}**\n{chunk_info}\n\n"
        
        yield json.dumps({"token": ref_text}) + "\n"

    # Parse Suggested Questions using Robust Regex
    suggested_questions = []
    
    explore_match = re.search(r"(?:Explore Further:?|🧐 Explore Further:?)", full_content, re.IGNORECASE)
    
    if explore_match:
        try:
            section_start = explore_match.end()
            questions_section = full_content[section_start:].split("### 📚 Reference Chunks")[0]
            
            potential_questions = re.findall(r"^[ \t]*(?:[-*]|\d+\.)?[ \t]*(.*?\?)[ \t]*$", questions_section, re.MULTILINE)
            
            for q in potential_questions:
                cleaned_q = re.sub(r"\*\*|_", "", q).strip()
                if cleaned_q and len(cleaned_q) > 10:
                    suggested_questions.append(cleaned_q)
        except Exception as e:
            print(f"Error parsing suggested questions with regex: {e}")
    
    yield json.dumps({"suggested_questions": suggested_questions[:4]}) + "\n"

    # Retrieve and yield OpenAI response
    if openai_future:
        try:
            openai_ans = openai_future.result(timeout=20)
        except Exception as e:
            openai_ans = f"Error or timeout fetching response from OpenAI: {str(e)}"
        finally:
            executor.shutdown(wait=False)
        
        yield json.dumps({"addl_ai": openai_ans}) + "\n"
    else:
        executor.shutdown(wait=False)
