# Sompo Risk MVP – Challenge FIAP × Sompo Seguros (Sprint 4)

Pipeline de risco para equipamentos: coleta → validação → features → modelo preditivo → score 0–100 → alertas preventivos → dashboard/relatórios, com segurança (RBAC, criptografia, auditoria).

## Executar
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # defina chave e senhas
python main.py                  # pipeline completo (dados simulados) ou: --input data/raw/sensores.csv
streamlit run src/reports/dashboard.py
pytest -q
```
Login demo (dev): `admin/admin123`, `analista/analista123`, `operador/operador123` (troque via `.env`).

## Formato do CSV de entrada
`machine_id, timestamp, temperature, humidity, vibration, load_pct, operating_hours, days_since_maintenance` (+ `failure` 0/1 para treino).

## Saídas
`outputs/alerts.csv`, `outputs/report.pdf`, tabelas `risk_scores` e `alerts` no SQLite, modelo em `src/models/artifacts/`.

Veja `docs/` para arquitetura, decisões e User Stories.
