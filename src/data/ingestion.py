"""Coleta: CSV/JSON (sensores, APIs exportadas) e simulador para demonstração."""
import numpy as np, pandas as pd
from pathlib import Path
from src.config import settings
from src.config.constants import TARGET
from src.utils.logger import get_logger
log = get_logger(__name__)

def load_csv(path) -> pd.DataFrame:
    log.info("Lendo CSV %s", path); return pd.read_csv(Path(path))

def load_json(path) -> pd.DataFrame:
    log.info("Lendo JSON %s", path); return pd.read_json(Path(path))

def simulate_data(n=settings.N_SIMULATED_READINGS, n_machines=settings.N_SIMULATED_MACHINES,
                  seed=settings.SEED, with_noise=True) -> pd.DataFrame:
    """Leituras sintéticas com falhas correlacionadas a vibração, temperatura e manutenção."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "machine_id": [f"MAQ-{i:03d}" for i in rng.integers(1, n_machines + 1, n)],
        "timestamp": pd.date_range("2026-01-01", periods=n, freq="30min"),
        "temperature": rng.normal(70, 15, n), "humidity": rng.normal(55, 18, n),
        "vibration": rng.gamma(2.0, 2.0, n), "load_pct": rng.normal(65, 20, n),
        "operating_hours": rng.uniform(100, 40000, n),
        "days_since_maintenance": rng.integers(0, 240, n).astype(float),
    })
    z = (-6.2 + 0.05 * (df.temperature - 70) + 0.35 * df.vibration + 0.02 * (df.load_pct - 65)
         + 0.012 * df.days_since_maintenance + 0.02 * (df.humidity - 55) + 0.00004 * df.operating_hours)
    df[TARGET] = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
    if with_noise:  # inconsistências reais: nulos, outliers, duplicatas
        for col in ("temperature", "vibration", "humidity"):
            df.loc[rng.choice(n, n // 50, replace=False), col] = np.nan
        df.loc[rng.choice(n, 5, replace=False), "temperature"] = 999
        df = pd.concat([df, df.sample(10, random_state=seed)], ignore_index=True)
    log.info("Simulados %d registros (taxa de falha %.1f%%)", len(df), 100 * df[TARGET].mean())
    return df
