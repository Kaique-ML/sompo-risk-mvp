from src.data.ingestion import simulate_data
from src.config.constants import RAW_COLUMNS, TARGET

def test_simulation_shape_and_columns():
    df = simulate_data(500, seed=1)
    assert set(RAW_COLUMNS + [TARGET]) <= set(df.columns) and len(df) >= 500

def test_simulation_reproducible():
    assert simulate_data(200, seed=3).equals(simulate_data(200, seed=3))
