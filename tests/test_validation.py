import pytest
from src.data.ingestion import simulate_data
from src.data.validation import validate
from src.utils.exceptions import DataValidationError

def test_validation_cleans_data():
    clean, rep = validate(simulate_data(800, seed=2))
    assert clean.isna().sum().sum() == 0 and clean.temperature.max() <= 150
    assert rep["duplicatas_removidas"] >= 1 and rep["outliers_corrigidos"] >= 1

def test_missing_columns_raise():
    with pytest.raises(DataValidationError):
        validate(simulate_data(50).drop(columns=["vibration"]))
