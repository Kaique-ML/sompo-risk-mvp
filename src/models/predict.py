import joblib, pandas as pd
from src.config import settings
from src.utils.exceptions import ModelNotTrainedError
from src.utils.helpers import score_to_level

def load_model(path=settings.MODEL_PATH):
    if not path.exists():
        raise ModelNotTrainedError("Modelo não encontrado. Execute: python main.py")
    return joblib.load(path)

def predict_scores(df: pd.DataFrame, artifact=None) -> pd.DataFrame:
    """Adiciona risk_score (0-100), risk_level e principal fator de risco por leitura."""
    artifact = artifact or load_model()
    model, feats = artifact["model"], artifact["features"]
    out = df.copy()
    out["risk_score"] = (model.predict_proba(out[feats])[:, 1] * 100).round(1)
    out["risk_level"] = out["risk_score"].map(score_to_level)
    imp = pd.Series(model.feature_importances_, index=feats)
    z = out[feats].sub(out[feats].mean()).div(out[feats].std().replace(0, 1))
    out["top_factor"] = (z.clip(lower=0) * imp).idxmax(axis=1)  # só desvios acima da média
    return out
