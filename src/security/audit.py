"""Log de auditoria append-only com encadeamento de hash (detecta adulteração)."""
import json, hashlib
from datetime import datetime, timezone
from src.config import settings

def _last_hash(path):
    if not path.exists() or path.stat().st_size == 0:
        return "GENESIS"
    return json.loads(path.read_text().strip().splitlines()[-1])["hash"]

def log_event(user: str, action: str, detail: str = "", path=None):
    path = path or settings.AUDIT_LOG
    rec = {"ts": datetime.now(timezone.utc).isoformat(), "user": user, "action": action,
           "detail": detail, "prev": _last_hash(path)}
    rec["hash"] = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()
    with open(path, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

def verify_chain(path=None) -> bool:
    path = path or settings.AUDIT_LOG; prev = "GENESIS"
    if not path.exists():
        return True
    for line in path.read_text().splitlines():
        rec = json.loads(line); h = rec.pop("hash")
        if rec["prev"] != prev or hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest() != h:
            return False
        prev = h
    return True
