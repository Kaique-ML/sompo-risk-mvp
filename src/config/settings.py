"""Configurações centralizadas (lidas de variáveis de ambiente)."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENV = os.getenv("SOMPO_ENV", "dev")
SEED = int(os.getenv("SOMPO_RANDOM_SEED", 42))
DB_PATH = Path(os.getenv("SOMPO_DB_PATH", ROOT / "data/processed/sompo.db"))
RAW_DIR, PROCESSED_DIR, SIM_DIR = (ROOT / "data" / d for d in ("raw", "processed", "simulated"))
MODEL_PATH = ROOT / "src/models/artifacts/risk_model.joblib"
OUTPUT_DIR = ROOT / "outputs"
LOG_DIR = ROOT / "logs"
AUDIT_LOG = LOG_DIR / "audit.jsonl"
ENCRYPTION_KEY = os.getenv("SOMPO_ENCRYPTION_KEY", "")
TEST_SIZE = 0.25
N_SIMULATED_MACHINES = 20
N_SIMULATED_READINGS = 3000
for p in (OUTPUT_DIR, LOG_DIR, RAW_DIR, PROCESSED_DIR, SIM_DIR, MODEL_PATH.parent):
    p.mkdir(parents=True, exist_ok=True)
