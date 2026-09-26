"""Validação e tratamento de inconsistências."""
import pandas as pd
from src.config.constants import RAW_COLUMNS, SENSOR_RANGES
from src.utils.exceptions import DataValidationError
from src.utils.logger import get_logger
log = get_logger(__name__)

def validate(df: pd.DataFrame):
    """Retorna (df_limpo, relatorio). Levanta DataValidationError se faltarem colunas."""
    missing = [c for c in RAW_COLUMNS if c not in df.columns]
    if missing:
        raise DataValidationError(f"Colunas ausentes: {missing}")
    df = df.copy(); rep = {"linhas_entrada": len(df)}
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["machine_id", "timestamp"])
    before = len(df); df = df.drop_duplicates(subset=["machine_id", "timestamp"])
    rep["duplicatas_removidas"] = before - len(df)
    rep["outliers_corrigidos"] = 0; rep["nulos_imputados"] = 0
    for col, (lo, hi) in SENSOR_RANGES.items():
        df[col] = pd.to_numeric(df[col], errors="coerce")
        bad = (df[col] < lo) | (df[col] > hi)
        rep["outliers_corrigidos"] += int(bad.sum()); df.loc[bad, col] = float("nan")
        rep["nulos_imputados"] += int(df[col].isna().sum())
        df[col] = df.groupby("machine_id")[col].transform(lambda s: s.fillna(s.median()))
        df[col] = df[col].fillna(df[col].median())
    rep["linhas_saida"] = len(df)
    log.info("Validação: %s", rep)
    return df.sort_values("timestamp").reset_index(drop=True), rep
