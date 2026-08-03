# app/services/audit.py
# Best-effort logging helpers. Failures here must NEVER break chat/auth.
import jwt
from sqlalchemy import text
from app.core.database import SessionLocal
from app.core.config import settings


def _uid_for(username):
    if not username:
        return None
    try:
        db = SessionLocal()
        r = db.execute(text("SELECT userId FROM user_master WHERE username=:u"), {"u": username}).fetchone()
        db.close()
        return r[0] if r else None
    except Exception:
        return None


def user_from_auth_header(auth_header: str):
    """(user_id, username) from a 'Bearer <jwt>' header, or (None, None)."""
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, None
    try:
        payload = jwt.decode(auth_header[7:], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        return _uid_for(username), username
    except Exception:
        return None, None


def save_chat_log(user_id, username, question, answer, model, endpoint):
    try:
        db = SessionLocal()
        db.execute(text(
            "INSERT INTO chat_log (user_id, username, question, answer, model, endpoint) "
            "VALUES (:uid,:un,:q,:a,:m,:e)"
        ), {"uid": user_id, "un": username, "q": question, "a": answer, "m": model, "e": endpoint})
        db.commit()
        db.close()
    except Exception as ex:
        print(f"[audit] save_chat_log failed: {ex}")


def log_activity(user_id, username, action, detail=""):
    try:
        db = SessionLocal()
        db.execute(text(
            "INSERT INTO activity_log (user_id, username, action, detail) VALUES (:uid,:un,:ac,:dt)"
        ), {"uid": user_id, "un": username, "ac": action, "dt": (detail or "")[:255]})
        db.commit()
        db.close()
    except Exception as ex:
        print(f"[audit] log_activity failed: {ex}")
