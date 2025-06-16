# tests/test_direct_revendeurs.py

import pytest
from flask import request
from app import create_app, db
from app.models import User, Product
from app.resources.revendeurs import RevendeursAPI, AuthenticateAPI
from unittest.mock import patch

@pytest.fixture
def app_context():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_revendeurs_get_direct_valid(app_context):
    with app_context.app_context():
        # Préparer la BDD
        user = User(email="revendeur@test.com", api_key="revendeurkey")
        product = Product(name="Café", description="Bon", price=5.0, model_url="")
        db.session.add_all([user, product])
        db.session.commit()

        # Mock l'en-tête x-api-key
        with patch("flask.request.headers.get", return_value="revendeurkey"):
            result = RevendeursAPI().get()
            assert len(result) == 1
            assert result[0].name == "Café"

def test_revendeurs_get_direct_missing_key(app_context):
    with app_context.app_context():
        with patch("flask.request.headers.get", return_value=None):
            with pytest.raises(Exception) as e:
                RevendeursAPI().get()
            assert "Clé API manquante" in str(e.value)

def test_revendeurs_get_direct_invalid_key(app_context):
    with app_context.app_context():
        # Aucun user correspondant
        with patch("flask.request.headers.get", return_value="invalidkey"):
            with pytest.raises(Exception) as e:
                RevendeursAPI().get()
            assert "Clé API invalide" in str(e.value)

def test_authenticate_post_valid(app_context):
    with app_context.app_context():
        db.session.add(User(email="auth@test.com", api_key="validkey"))
        db.session.commit()

        with patch("flask.request.headers.get", return_value="validkey"):
            res, code = AuthenticateAPI().post()
            assert code == 200
            assert res["message"] == "Authentification réussie"

def test_authenticate_post_missing_key(app_context):
    with app_context.app_context():
        with patch("flask.request.headers.get", return_value=None):
            with pytest.raises(Exception) as e:
                AuthenticateAPI().post()
            assert "Clé API manquante" in str(e.value)

def test_authenticate_post_invalid_key(app_context):
    with app_context.app_context():
        with patch("flask.request.headers.get", return_value="wrongkey"):
            with pytest.raises(Exception) as e:
                AuthenticateAPI().post()
            assert "Clé invalide" in str(e.value)
