# app/api/routers/chat.py
#
# =====================================================================
# PRESERVED CHAT ENDPOINTS — The embedding logic is untouched.
# Only the routing layer has been reorganized.
# =====================================================================

from fastapi import APIRouter, BackgroundTasks, File, UploadFile, Form
from fastapi.responses import StreamingResponse
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
from configure import get_subject_files

router = APIRouter(prefix="/api", tags=["Chat & Knowledge Base"])


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
    query: str = Form(...),
    history: str = Form("[]"),
    subject: Optional[str] = Form(None),
    year: Optional[str] = Form(None),
    branch: Optional[str] = Form(None),
    semester: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    """
    Chat endpoint that performs RAG (Retrieval Augmented Generation).
    Accepts text queries and optional images.
    """
    try:
        history_list = json.loads(history)
        prompt = query
        
        # Query knowledge base with exception safety
        try:
            context, retrieved_chunks_info = query_knowledge_base(
                prompt=prompt,
                year=year,
                branch=branch,
                semester=semester,
                subject=subject
            )
        except Exception as e:
            print(f"[Chat] Knowledge base query failed: {e}. Falling back to empty context.")
            context = ""
            retrieved_chunks_info = []
        
        # Build the augmented prompt
        final_prompt = build_prompt(context, prompt)
        
        # Process image if present
        image_bytes = None
        if image:
            content = await image.read()
            image_bytes = content
        
        # Return streaming response
        return StreamingResponse(
            generate_response_stream(final_prompt, image_bytes, retrieved_chunks_info, raw_query=prompt, subject=subject),
            media_type="application/x-ndjson"
        )

    except Exception as e:
        print(f"Error: {e}")
        def error_generator():
            yield json.dumps({"token": f"Error: {str(e)}"}) + "\n"
        return StreamingResponse(error_generator(), media_type="application/x-ndjson")
