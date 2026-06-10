# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "user_master"

    userId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    user_type = Column(String(50))
    login_time = Column(DateTime)
    login_status = Column(Integer)
    last_logout_time = Column(DateTime)
    status = Column(Integer, default=1)
    is_locked = Column(DateTime)
