from src.data.ingestion import simulate_data
from src.data.validation import validate
from src.data.transformation import engineer_features
from src.models.train import train
from src.models.predict import predict_scores

def _data():
    return engineer_features(validate(simulate_data(2500, seed=5))[0])

def test_train_and_predict(tmp_path):
    df = _data(); model, m = train(df, path=tmp_path / "m.joblib")
    assert m["roc_auc"] > 0.7
    import joblib
    out = predict_scores(df, joblib.load(tmp_path / "m.joblib"))
    assert out.risk_score.between(0, 100).all() and out.risk_level.notna().all()
