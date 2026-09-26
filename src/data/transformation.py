"""Feature engineering."""
import pandas as pd
from src.config.constants import MAINTENANCE_LIMIT_DAYS, HUMIDITY_LIMIT

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["thermal_stress"] = df["temperature"] * df["load_pct"] / 100
    df["vib_per_load"] = df["vibration"] / (df["load_pct"].clip(lower=0) + 1)
    df["maintenance_overdue"] = (df["days_since_maintenance"] > MAINTENANCE_LIMIT_DAYS).astype(int)
    df["humidity_high"] = (df["humidity"] > HUMIDITY_LIMIT).astype(int)
    return df
