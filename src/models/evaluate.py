from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

def evaluate(model, X, y) -> dict:
    proba = model.predict_proba(X)[:, 1]; pred = (proba >= 0.5).astype(int)
    return {"precision": round(precision_score(y, pred, zero_division=0), 3),
            "recall": round(recall_score(y, pred, zero_division=0), 3),
            "f1": round(f1_score(y, pred, zero_division=0), 3),
            "roc_auc": round(roc_auc_score(y, proba), 3),
            "confusion_matrix": confusion_matrix(y, pred).tolist()}
