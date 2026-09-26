"""Criptografia simétrica (Fernet/AES) e pseudonimização de identificadores."""
import hashlib
from cryptography.fernet import Fernet
from src.config import settings
from src.utils.logger import get_logger
log = get_logger(__name__)
_key = settings.ENCRYPTION_KEY.encode() if settings.ENCRYPTION_KEY else Fernet.generate_key()
if not settings.ENCRYPTION_KEY:
    log.warning("SOMPO_ENCRYPTION_KEY ausente: chave efêmera (dados não recuperáveis após reinício).")
_f = Fernet(_key)

def encrypt(value: str) -> str: return _f.encrypt(value.encode()).decode()
def decrypt(token: str) -> str: return _f.decrypt(token.encode()).decode()
def pseudonymize(value: str) -> str:
    return hashlib.sha256((value + _key.decode()).encode()).hexdigest()[:12]
