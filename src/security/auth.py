"""Autenticação (PBKDF2) e autorização por perfil (RBAC)."""
import os, hashlib, hmac
from src.config.constants import ROLES
from src.security.audit import log_event
from src.utils.exceptions import AuthenticationError, AuthorizationError

def _hash(pw: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, 200_000)

def _mk(pw):
    s = os.urandom(16); return s, _hash(pw, s)

_USERS = {  # demo: em produção, usar IdP corporativo/DB
    "admin": ("admin", *_mk(os.getenv("SOMPO_ADMIN_PASSWORD", "admin123"))),
    "analista": ("analista", *_mk(os.getenv("SOMPO_ANALYST_PASSWORD", "analista123"))),
    "operador": ("operador", *_mk(os.getenv("SOMPO_OPERATOR_PASSWORD", "operador123"))),
}

def authenticate(user: str, password: str) -> str:
    """Retorna o perfil (role) ou levanta AuthenticationError."""
    rec = _USERS.get(user)
    if not rec or not hmac.compare_digest(rec[2], _hash(password, rec[1])):
        log_event(user or "?", "login_failed"); raise AuthenticationError("Credenciais inválidas")
    log_event(user, "login_ok"); return rec[0]

def authorize(role: str, permission: str):
    if permission not in ROLES.get(role, set()):
        raise AuthorizationError(f"Perfil '{role}' sem permissão '{permission}'")
