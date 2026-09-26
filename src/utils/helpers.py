from src.config.constants import RISK_LEVELS

def score_to_level(score: float) -> str:
    for lo, hi, name in RISK_LEVELS:
        if lo <= score < hi:
            return name
    return "CRÍTICO"
