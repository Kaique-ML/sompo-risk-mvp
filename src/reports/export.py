import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from src.config import settings

def to_csv(df, name="report.csv"):
    p = settings.OUTPUT_DIR / name; df.to_csv(p, index=False); return p

def to_pdf(scored, alerts, name="report.pdf"):
    """PDF executivo: distribuição de risco, top máquinas e tabela de alertas."""
    p = settings.OUTPUT_DIR / name
    with PdfPages(p) as pdf:
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
        scored["risk_level"].value_counts().reindex(["BAIXO", "MÉDIO", "ALTO", "CRÍTICO"]).fillna(0).plot.bar(ax=ax[0], color="#2a6fdb")
        ax[0].set_title("Leituras por nível de risco")
        scored.groupby("machine_id")["risk_score"].mean().nlargest(10).plot.barh(ax=ax[1], color="#d64545")
        ax[1].set_title("Top 10 máquinas (score médio)"); fig.tight_layout(); pdf.savefig(fig); plt.close(fig)
        fig, ax = plt.subplots(figsize=(11, 4.5)); ax.axis("off"); ax.set_title("Alertas preventivos")
        if len(alerts):
            t = alerts.head(12).assign(recommendation=lambda d: d.recommendation.str[:55],
                                       timestamp=lambda d: d.timestamp.astype(str).str[:16])
            tb = ax.table(cellText=t.values, colLabels=t.columns, loc="center")
            tb.auto_set_font_size(False); tb.set_fontsize(6)
        pdf.savefig(fig); plt.close(fig)
    return p
