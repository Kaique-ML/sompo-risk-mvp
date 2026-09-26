"""Ponto de entrada: pipeline completo (coleta → validação → features → modelo → alertas → relatórios)."""
import argparse
from src.config import settings
from src.data import ingestion, validation, transformation, database
from src.models import train, predict
from src.reports import alerts, export
from src.security.audit import log_event
from src.utils.logger import get_logger
log = get_logger("main")

def run(input_csv=None, n=settings.N_SIMULATED_READINGS):
    df = ingestion.load_csv(input_csv) if input_csv else ingestion.simulate_data(n)
    if not input_csv:
        df.to_csv(settings.SIM_DIR / "sensors_simulated.csv", index=False)
    clean, report = validation.validate(df)
    feats = transformation.engineer_features(clean)
    feats.to_csv(settings.PROCESSED_DIR / "features.csv", index=False)
    _, metrics = train.train(feats)
    scored = predict.predict_scores(feats)
    database.save_table(scored, "risk_scores")
    al = alerts.generate_alerts(scored); database.save_table(al, "alerts")
    export.to_csv(al, "alerts.csv"); pdf = export.to_pdf(scored, al)
    log_event("system", "pipeline_run", f"{len(scored)} leituras, {len(al)} alertas")
    log.info("Concluído | alertas=%d | PDF=%s", len(al), pdf)
    return {"validation": report, "metrics": metrics, "alerts": len(al)}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Sompo Risk MVP")
    ap.add_argument("--input", help="CSV de sensores (padrão: dados simulados)")
    ap.add_argument("--n", type=int, default=settings.N_SIMULATED_READINGS)
    print(run(ap.parse_args().input, ap.parse_args().n))
    print("Dashboard: streamlit run src/reports/dashboard.py")
