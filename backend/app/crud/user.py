from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def get_user_by_identifier(db: Session, identifier: str):
    """Query the database for a user by their username or userId."""
    # Try to see if identifier is a numeric userId
    is_numeric = identifier.isdigit()
    
    if is_numeric:
        return db.query(User).filter(
            or_(User.username == identifier, User.userId == int(identifier))
        ).first()
    else:
        return db.query(User).filter(User.username == identifier).first()


def get_user_by_id(db: Session, user_id: int):
    """Query the database for a user by their ID."""
    return db.query(User).filter(User.userId == user_id).first()


def create_user(db: Session, user: UserCreate):
    """Create a new user in the database with a hashed password."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        password=hashed_password,
        user_type=user.user_type,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
