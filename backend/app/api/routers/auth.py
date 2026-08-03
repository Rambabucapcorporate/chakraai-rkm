# app/api/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.api.dependencies import get_db, get_current_user
from app.crud.user import get_user_by_identifier
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import Token
from app.services.audit import log_activity

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user with username/userId and password.
    Returns a JWT access token on success.
    """
    # Find user in database
    db_user = get_user_by_identifier(db, identifier=user.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID or Username doesn't exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is inactive (status = 0)
    if db_user.status == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive. Contact RKMVC Admin to activate your account.",
        )
        
    # Check if user is locked (is_locked = 1 or is a valid datetime)
    is_locked = False
    if isinstance(db_user.is_locked, int):
        is_locked = (db_user.is_locked == 1)
    elif db_user.is_locked is not None:
        is_locked = True
        
    if is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is locked. Please contact administrator.",
        )
    
    # Verify password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password is wrong",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )

    log_activity(db_user.userId, db_user.username, "login")

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    """
    Get the currently authenticated user's profile.
    Requires a valid JWT Bearer token.
    """
    return current_user
