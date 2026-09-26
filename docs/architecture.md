# Arquitetura

```
Sensores/CSV/Simulador → ingestion → validation → transformation → models(train/predict)
                                                        │                    │
                                                   database (SQLite) ← risk_scores
                                                        │
                        alerts → export (CSV/PDF) → dashboard (Streamlit, RBAC)
Transversal: security (auth/RBAC, encryption, audit hash-chain), utils (logger, exceptions)
```
Fluxo: `main.py` orquestra o pipeline; o dashboard lê apenas do banco e exige login.
