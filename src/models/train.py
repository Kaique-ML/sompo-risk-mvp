import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from src.config import settings
from src.config.constants import FEATURES, TARGET
from src.models.evaluate import evaluate
from src.utils.logger import get_logger
log = get_logger(__name__)

def train(df, path=settings.MODEL_PATH):
    """RandomForest com class_weight balanceado (falhas são raras); salva artefato e retorna métricas."""
    X, y = df[FEATURES], df[TARGET]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=settings.TEST_SIZE,
                                          stratify=y, random_state=settings.SEED)
    model = RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_leaf=5,
                                   class_weight="balanced", random_state=settings.SEED, n_jobs=-1)
    model.fit(Xtr, ytr)
    metrics = evaluate(model, Xte, yte)
    joblib.dump({"model": model, "features": FEATURES, "metrics": metrics}, path)
    log.info("Modelo salvo em %s | métricas: %s", path, metrics)
    return model, metrics
