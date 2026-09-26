import main
from src.security.auth import authenticate, authorize
from src.security.audit import verify_chain
from src.security.encryption import encrypt, decrypt
from src.utils.exceptions import AuthenticationError, AuthorizationError
import pytest

def test_full_pipeline(tmp_path, monkeypatch):
    monkeypatch.setattr("src.config.settings.DB_PATH", tmp_path / "t.db")
    res = main.run(n=1500)
    assert res["metrics"]["roc_auc"] > 0.7 and res["alerts"] >= 0
    assert verify_chain()

def test_security():
    assert authenticate("admin", "admin123") == "admin"
    with pytest.raises(AuthenticationError): authenticate("admin", "x")
    with pytest.raises(AuthorizationError): authorize("operador", "export")
    assert decrypt(encrypt("segredo")) == "segredo"
