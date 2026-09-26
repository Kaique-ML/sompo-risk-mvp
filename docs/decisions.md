# Decisões técnicas
- **RandomForest**: robusto a escalas/não linearidades, dá `feature_importances_` (explicabilidade dos alertas), `class_weight=balanced` para falhas raras.
- **SQLite**: zero configuração p/ MVP; camada `database.py` isolada facilita migrar para PostgreSQL.
- **Dados simulados**: reprodutíveis (seed) com ruído injetado (nulos, outliers, duplicatas) para demonstrar a validação.
- **Segurança**: PBKDF2 + RBAC (admin/analista/operador), Fernet (AES) para dados sensíveis, auditoria com hash encadeado.
- **Streamlit + Plotly**: dashboard rápido e interativo; PDF via Matplotlib (sem dependências pesadas).
- **Limitação**: score calibrado sobre dados sintéticos; substituir por histórico real de sinistros/falhas antes de uso em produção.
