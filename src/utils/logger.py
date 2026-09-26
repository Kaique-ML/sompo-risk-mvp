import logging, sys
from src.config import settings

def get_logger(name: str) -> logging.Logger:
    log = logging.getLogger(name)
    if not log.handlers:
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        for h in (logging.StreamHandler(sys.stdout), logging.FileHandler(settings.LOG_DIR / "app.log")):
            h.setFormatter(fmt); log.addHandler(h)
        log.setLevel(logging.DEBUG if settings.ENV == "dev" else logging.INFO)
        log.propagate = False
    return log
