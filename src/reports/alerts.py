import pandas as pd
from src.config.constants import RECOMMENDATIONS

def generate_alerts(scored: pd.DataFrame, min_level=("ALTO", "CRÍTICO")) -> pd.DataFrame:
    """Último estado de cada máquina em nível relevante + recomendação preventiva."""
    last = scored.sort_values("timestamp").groupby("machine_id").tail(1)
    al = last[last["risk_level"].isin(min_level)].copy()
    al["recommendation"] = al["top_factor"].map(RECOMMENDATIONS).fillna("Inspeção geral recomendada.")
    return al.sort_values("risk_score", ascending=False)[
        ["machine_id", "timestamp", "risk_score", "risk_level", "top_factor", "recommendation"]]
