# app/api/routers/admin.py
# Admin dashboard API. All routes require an admin user (user_type '1').
import subprocess
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def require_admin(current_user=Depends(get_current_user)):
    if str(getattr(current_user, "user_type", "")) != "1":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/stats")
def stats(db: Session = Depends(get_db), _a=Depends(require_admin)):
    def sc(q, p=None):
        try:
            return db.execute(text(q), p or {}).scalar()
        except Exception:
            return 0
    return {
        "total_users": sc("SELECT COUNT(*) FROM user_master"),
        "active_users": sc("SELECT COUNT(*) FROM user_master WHERE status='1'"),
        "locked_users": sc("SELECT COUNT(*) FROM user_master WHERE is_locked IS NOT NULL"),
        "users_by_type": [{"type": r[0], "count": r[1]} for r in db.execute(text(
            "SELECT user_type, COUNT(*) FROM user_master GROUP BY user_type ORDER BY COUNT(*) DESC")).fetchall()],
        "total_chats": sc("SELECT COUNT(*) FROM chat_log"),
        "chats_today": sc("SELECT COUNT(*) FROM chat_log WHERE created_at >= CURDATE()"),
        "logins_today": sc("SELECT COUNT(*) FROM activity_log WHERE action='login' AND created_at >= CURDATE()"),
        "active_chat_users_today": sc("SELECT COUNT(DISTINCT user_id) FROM chat_log WHERE created_at >= CURDATE()"),
        # student = user_type '2'; join on user_id (int) to avoid username collation mismatch
        "active_students_today": sc(
            "SELECT COUNT(DISTINCT c.user_id) FROM chat_log c JOIN user_master u ON c.user_id = u.userId "
            "WHERE c.created_at >= CURDATE() AND u.user_type = '2'"),
        "distinct_login_users_today": sc(
            "SELECT COUNT(DISTINCT user_id) FROM activity_log WHERE action='login' AND created_at >= CURDATE()"),
        # answer latency (populated for chats after latency logging was added)
        "avg_answer_ms_today": sc(
            "SELECT ROUND(AVG(latency_ms)) FROM chat_log WHERE created_at >= CURDATE() AND latency_ms IS NOT NULL"),
        "answers_measured_today": sc(
            "SELECT COUNT(*) FROM chat_log WHERE created_at >= CURDATE() AND latency_ms IS NOT NULL"),
        "avg_answer_ms_7d": sc(
            "SELECT ROUND(AVG(latency_ms)) FROM chat_log WHERE created_at >= (CURDATE() - INTERVAL 6 DAY) AND latency_ms IS NOT NULL"),
        # thumbs-up/down feedback (RL / quality signal)
        "feedback_up_today": sc("SELECT COUNT(*) FROM chat_log WHERE created_at >= CURDATE() AND feedback = 1"),
        "feedback_down_today": sc("SELECT COUNT(*) FROM chat_log WHERE created_at >= CURDATE() AND feedback = -1"),
        "feedback_up_total": sc("SELECT COUNT(*) FROM chat_log WHERE feedback = 1"),
        "feedback_down_total": sc("SELECT COUNT(*) FROM chat_log WHERE feedback = -1"),
    }


@router.get("/gpu")
def gpu(_a=Depends(require_admin)):
    def run(args):
        try:
            return subprocess.run(args, capture_output=True, text=True, timeout=8).stdout.strip()
        except Exception:
            return ""
    gpus = []
    out = run(["nvidia-smi",
               "--query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw,power.limit",
               "--format=csv,noheader,nounits"])
    for line in out.splitlines():
        p = [x.strip() for x in line.split(",")]
        if len(p) >= 8:
            gpus.append({"index": p[0], "name": p[1], "temp_c": p[2], "util_pct": p[3],
                         "mem_used_mib": p[4], "mem_total_mib": p[5],
                         "power_w": p[6], "power_limit_w": p[7]})
    procs = []
    out = run(["nvidia-smi", "--query-compute-apps=pid,used_memory,process_name",
               "--format=csv,noheader,nounits"])
    for line in out.splitlines():
        p = [x.strip() for x in line.split(",")]
        if len(p) >= 3:
            procs.append({"pid": p[0], "mem_mib": p[1], "name": p[2]})
    services = {}
    for s in ["rkm-vllm", "ollama", "chakra-backend"]:
        try:
            services[s] = subprocess.run(["systemctl", "is-active", s],
                                         capture_output=True, text=True, timeout=5).stdout.strip()
        except Exception:
            services[s] = "unknown"
    return {"gpus": gpus, "processes": procs, "services": services, "nvidia_smi_ok": bool(gpus)}


@router.get("/users")
def users(db: Session = Depends(get_db), _a=Depends(require_admin),
          q: str = Query(""), user_type: str = Query(""),
          limit: int = Query(50, le=200), offset: int = Query(0)):
    where = "WHERE 1=1"
    params = {}
    if q:
        where += " AND username LIKE :q"
        params["q"] = f"%{q}%"
    if user_type:
        where += " AND user_type = :ut"
        params["ut"] = user_type
    total = db.execute(text(f"SELECT COUNT(*) FROM user_master {where}"), params).scalar()
    p2 = dict(params, lim=limit, off=offset)
    rows = db.execute(text(
        f"SELECT userId,username,user_type,status,login_time,login_status,last_logout_time,is_locked "
        f"FROM user_master {where} ORDER BY login_time DESC LIMIT :lim OFFSET :off"), p2).fetchall()
    return {"total": total, "users": [{
        "userId": r[0], "username": r[1], "user_type": r[2], "status": r[3],
        "login_time": str(r[4]) if r[4] else None, "login_status": r[5],
        "last_logout_time": str(r[6]) if r[6] else None,
        "is_locked": str(r[7]) if r[7] else None} for r in rows]}


@router.get("/chats")
def chats(db: Session = Depends(get_db), _a=Depends(require_admin),
          username: str = Query(""), limit: int = Query(50, le=200), offset: int = Query(0)):
    where = "WHERE 1=1"
    params = {}
    if username:
        where += " AND username LIKE :u"
        params["u"] = f"%{username}%"
    total = db.execute(text(f"SELECT COUNT(*) FROM chat_log {where}"), params).scalar()
    p2 = dict(params, lim=limit, off=offset)
    rows = db.execute(text(
        f"SELECT id,user_id,username,question,answer,model,endpoint,created_at "
        f"FROM chat_log {where} ORDER BY created_at DESC LIMIT :lim OFFSET :off"), p2).fetchall()
    return {"total": total, "chats": [{
        "id": r[0], "user_id": r[1], "username": r[2], "question": r[3],
        "answer": (r[4] or "")[:6000], "model": r[5], "endpoint": r[6],
        "created_at": str(r[7])} for r in rows]}


@router.get("/activity")
def activity(db: Session = Depends(get_db), _a=Depends(require_admin),
             username: str = Query(""), action: str = Query(""),
             limit: int = Query(100, le=500), offset: int = Query(0)):
    where = "WHERE 1=1"
    params = {}
    if username:
        where += " AND username LIKE :u"
        params["u"] = f"%{username}%"
    if action:
        where += " AND action = :a"
        params["a"] = action
    total = db.execute(text(f"SELECT COUNT(*) FROM activity_log {where}"), params).scalar()
    p2 = dict(params, lim=limit, off=offset)
    rows = db.execute(text(
        f"SELECT id,user_id,username,action,detail,created_at "
        f"FROM activity_log {where} ORDER BY created_at DESC LIMIT :lim OFFSET :off"), p2).fetchall()
    return {"total": total, "activity": [{
        "id": r[0], "user_id": r[1], "username": r[2], "action": r[3],
        "detail": r[4], "created_at": str(r[5])} for r in rows]}
