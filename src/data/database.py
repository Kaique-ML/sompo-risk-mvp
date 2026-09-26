"""Persistência em SQLite (trocável por PostgreSQL via SQLAlchemy)."""
import sqlite3, pandas as pd
from contextlib import contextmanager
from src.config import settings
from src.utils.exceptions import DatabaseError

@contextmanager
def connect(path=None):
    conn = sqlite3.connect(path or settings.DB_PATH)
    try:
        yield conn; conn.commit()
    except Exception as e:
        conn.rollback(); raise DatabaseError(str(e)) from e
    finally:
        conn.close()

def save_table(df: pd.DataFrame, table: str, if_exists="replace", path=None):
    with connect(path) as c:
        df.to_sql(table, c, if_exists=if_exists, index=False)

def load_table(table: str, path=None) -> pd.DataFrame:
    with connect(path) as c:
        return pd.read_sql(f"SELECT * FROM {table}", c)
