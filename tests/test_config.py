import os
import importlib

def test_config_defaults(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("API_WEBSHOP_KEY", raising=False)

    if "app.config" in importlib.sys.modules:
        importlib.reload(importlib.import_module("app.config"))
    from app.config import Config

    assert Config.SQLALCHEMY_DATABASE_URI == "sqlite:///mon_projet.db"
    assert Config.SECRET_KEY == "default_secret_key"
    assert Config.API_WEBSHOP_KEY == "webshop_default_key"
