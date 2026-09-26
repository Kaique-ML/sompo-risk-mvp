"""Dashboard Streamlit. Execute: streamlit run src/reports/dashboard.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import pandas as pd
import streamlit as st, plotly.express as px
from src.data.database import load_table
from src.reports.alerts import generate_alerts
from src.reports.export import to_csv
from src.security.auth import authenticate, authorize
from src.security.audit import log_event
from src.utils.exceptions import SompoError

st.set_page_config(page_title="Sompo Risk MVP", layout="wide")
if "role" not in st.session_state:
    st.title("🔐 Sompo Risk – Acesso")
    u, p = st.text_input("Usuário"), st.text_input("Senha", type="password")
    if st.button("Entrar"):
        try:
            st.session_state.update(role=authenticate(u, p), user=u); st.rerun()
        except SompoError as e:
            st.error(str(e))
    st.stop()

role, user = st.session_state.role, st.session_state.user
scored = load_table("risk_scores"); scored["timestamp"] = pd.to_datetime(scored["timestamp"])
alerts = generate_alerts(scored)
st.title("🛡️ Monitoramento de Risco de Equipamentos"); st.caption(f"Usuário: {user} ({role})")
k = st.columns(3)
k[0].metric("Máquinas", scored.machine_id.nunique()); k[1].metric("Alertas ativos", len(alerts))
k[2].metric("Score médio", f"{scored.risk_score.mean():.1f}")
st.subheader("🚨 Alertas e recomendações"); st.dataframe(alerts, use_container_width=True)
if role != "operador":  # perfis analítico/gestão veem histórico completo
    m = st.selectbox("Máquina", sorted(scored.machine_id.unique()))
    st.plotly_chart(px.line(scored[scored.machine_id == m], x="timestamp", y="risk_score",
                            title=f"Evolução do risco – {m}"), use_container_width=True)
    st.plotly_chart(px.histogram(scored, x="risk_score", color="risk_level",
                                 title="Distribuição de scores"), use_container_width=True)
    if st.button("Exportar CSV"):
        authorize(role, "export"); log_event(user, "export_csv"); st.success(f"Salvo em {to_csv(alerts)}")
