# app/schemas/chat.py
from pydantic import BaseModel
from typing import List


class LoadRequest(BaseModel):
    """Schema for loading knowledge base files."""
    filenames: List[str]


class SubjectSelectionRequest(BaseModel):
    """Schema for selecting a subject to load."""
    year: str
    branch: str
    semester: str
    subject: str


class ChatResponse(BaseModel):
    """Schema for chat response."""
    response: str
    suggested_questions: List[str] = []
