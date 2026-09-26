"""Constantes do domínio: sensores, features e níveis de risco."""
RAW_COLUMNS = ["machine_id", "timestamp", "temperature", "humidity", "vibration",
               "load_pct", "operating_hours", "days_since_maintenance"]
TARGET = "failure"
SENSOR_RANGES = {  # (min, max) fisicamente plausíveis
    "temperature": (-10, 150), "humidity": (0, 100), "vibration": (0, 50),
    "load_pct": (0, 120), "operating_hours": (0, 200000), "days_since_maintenance": (0, 3650),
}
BASE_FEATURES = ["temperature", "humidity", "vibration", "load_pct",
                 "operating_hours", "days_since_maintenance"]
ENGINEERED_FEATURES = ["thermal_stress", "vib_per_load", "maintenance_overdue", "humidity_high"]
FEATURES = BASE_FEATURES + ENGINEERED_FEATURES
RISK_LEVELS = [(0, 30, "BAIXO"), (30, 60, "MÉDIO"), (60, 80, "ALTO"), (80, 101, "CRÍTICO")]
MAINTENANCE_LIMIT_DAYS = 90
HUMIDITY_LIMIT = 80
ROLES = {"admin": {"view_all", "export", "manage_users"},
         "analista": {"view_all", "export"},
         "operador": {"view_alerts"}}
RECOMMENDATIONS = {
    "vibration": "Inspecionar rolamentos, alinhamento e fixações do equipamento.",
    "temperature": "Verificar refrigeração/lubrificação e reduzir carga até normalizar.",
    "humidity": "Checar vedação e ambiente; risco de corrosão e curto-circuito.",
    "days_since_maintenance": "Agendar manutenção preventiva (prazo vencido).",
    "load_pct": "Redistribuir carga operacional para evitar sobrecarga.",
    "operating_hours": "Avaliar vida útil restante e troca de componentes.",
    "thermal_stress": "Reduzir carga e verificar refrigeração (estresse térmico).",
    "vib_per_load": "Inspecionar rolamentos: vibração alta para a carga atual.",
    "maintenance_overdue": "Agendar manutenção preventiva (prazo vencido).",
    "humidity_high": "Checar vedação e ambiente; umidade acima do limite.",
}
