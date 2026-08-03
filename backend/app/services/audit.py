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


def save_chat_log(user_id, username, question, answer, model, endpoint, latency_ms=None):
    """Insert a chat row and return its id (used to attach feedback), or None on failure."""
    try:
        db = SessionLocal()
        res = db.execute(text(
            "INSERT INTO chat_log (user_id, username, question, answer, model, endpoint, latency_ms) "
            "VALUES (:uid,:un,:q,:a,:m,:e,:lat)"
        ), {"uid": user_id, "un": username, "q": question, "a": answer, "m": model,
            "e": endpoint, "lat": latency_ms})
        cid = res.lastrowid
        db.commit()
        db.close()
        return cid
    except Exception as ex:
        print(f"[audit] save_chat_log failed: {ex}")
        return None


def save_feedback(chat_id, rating, user_id=None):
    """Record a thumbs up (1) / down (-1) / clear (0) rating on a chat_log row. Best-effort."""
    try:
        val = None if rating == 0 else rating
        db = SessionLocal()
        if user_id:
            # only let a user rate their own answers (or anonymous rows)
            db.execute(text(
                "UPDATE chat_log SET feedback=:r, feedback_at=NOW() "
                "WHERE id=:cid AND (user_id=:uid OR user_id IS NULL)"),
                {"r": val, "cid": chat_id, "uid": user_id})
        else:
            db.execute(text(
                "UPDATE chat_log SET feedback=:r, feedback_at=NOW() WHERE id=:cid"),
                {"r": val, "cid": chat_id})
        db.commit()
        db.close()
        return True
    except Exception as ex:
        print(f"[audit] save_feedback failed: {ex}")
        return False


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
