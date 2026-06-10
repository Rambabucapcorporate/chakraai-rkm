# app/schemas/token.py
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Schema for the JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for the data encoded inside the JWT."""
    username: Optional[str] = None
