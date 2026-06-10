# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for user registration request."""
    username: str
    password: str
    user_type: Optional[str] = "student"


class UserLogin(BaseModel):
    """Schema for user login request."""
    username: str # This will accept either username or userId
    password: str


class UserResponse(BaseModel):
    """Schema for user data returned in API responses."""
    userId: int
    username: str
    user_type: Optional[str] = None
    status: Optional[int] = 1
    is_locked: Optional[Union[int, datetime]] = 0

    class Config:
        from_attributes = True
