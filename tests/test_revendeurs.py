import os
from unittest import mock
import pytest
from datetime import datetime

import requests
from app import db
from app.models import User, Product

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

# -------------------------------
# TESTS REVENDEURS AVEC MOCK ACTIVÉ
# -------------------------------

def test_revendeur_list_with_valid_key(client, setup_user, mocker):
    os.environ["USE_MOCK_PRODUCTS"] = "true"
    setup_user(email="revendeur@test.com", api_key="revendeur_key")
    mock_data = [{
        "id": "1",
        "name": "Produit Revendeur",
        "details": {"description": "Desc", "price": "5.0"},
        "stock": 10,
        "createdAt": datetime.strptime("2024-01-01", "%Y-%m-%d")
    }]
    mocker.patch("app.resources.revendeurs.requests.get", return_value=MockResponse(mock_data))
    res = client.get("/api/revendeurs/products", headers={"x-api-key": "revendeur_key"})
    assert res.status_code == 200
    assert res.get_json()[0]["name"] == "Produit Revendeur"
    del os.environ["USE_MOCK_PRODUCTS"]

def test_revendeur_detail_with_valid_key(client, setup_user, mocker):
    os.environ["USE_MOCK_PRODUCTS"] = "true"
    setup_user(email="revendeur@test.com", api_key="revendeur_key")
    mock_data = {
        "id": "1",
        "name": "Produit Détail",
        "details": {"description": "Desc Détail", "price": "15.0"},
        "stock": 5,
        "createdAt": datetime.strptime("2024-01-01", "%Y-%m-%d")
    }
    mocker.patch("app.resources.revendeurs.requests.get", return_value=MockResponse(mock_data))
    res = client.get("/api/revendeurs/products/1", headers={"x-api-key": "revendeur_key"})
    assert res.status_code == 200
    assert res.get_json()["stock"] == 5
    del os.environ["USE_MOCK_PRODUCTS"]

def test_revendeurs_get_direct_valid(client, setup_user, mocker):
    os.environ["USE_MOCK_PRODUCTS"] = "true"
    setup_user(email="revendeur@test.com", api_key="valid_key")
    mock_data = [{
        "id": "1",
        "name": "Produit Test",
        "details": {"description": "Desc", "price": "1.0"},
        "stock": 20,
        "createdAt": datetime.strptime("2024-01-01", "%Y-%m-%d")
    }]
    mocker.patch("app.resources.revendeurs.requests.get", return_value=MockResponse(mock_data))
    res = client.get("/api/revendeurs/products", headers={"x-api-key": "valid_key"})
    assert res.status_code == 200
    assert res.get_json()[0]["name"] == "Produit Test"
    del os.environ["USE_MOCK_PRODUCTS"]

# -------------------------------
# TESTS D’AUTH / ERREURS
# -------------------------------

def test_revendeurs_get_direct_missing_key(client):
    res = client.get("/api/revendeurs/products")
    assert res.status_code == 401

def test_revendeurs_get_direct_invalid_key(client):
    res = client.get("/api/revendeurs/products", headers={"x-api-key": "wrong"})
    assert res.status_code == 401

def test_authenticate_post_valid(client, setup_user):
    setup_user(email="auth@test.com", api_key="authkey")
    res = client.post("/api/revendeurs/authenticate", headers={"x-api-key": "authkey"})
    assert res.status_code == 200

def test_authenticate_post_missing_key(client):
    res = client.post("/api/revendeurs/authenticate")
    assert res.status_code == 400

def test_authenticate_post_invalid_key(client):
    res = client.post("/api/revendeurs/authenticate", headers={"x-api-key": "invalid"})
    assert res.status_code == 401

def test_revendeurs_mock_api_down(client, setup_user, mocker):
    os.environ["USE_MOCK_PRODUCTS"] = "true"
    setup_user(email="revendeur@test.com", api_key="fail_key")
    mocker.patch("app.resources.revendeurs.requests.get", side_effect=requests.RequestException("DOWN"))

    res = client.get("/api/revendeurs/products", headers={"x-api-key": "fail_key"})
    assert res.status_code == 503
    del os.environ["USE_MOCK_PRODUCTS"]


# def test_revendeurs_get_from_db_when_mock_disabled(client, setup_user, app):
#     os.environ["USE_MOCK_PRODUCTS"] = "false"
#     setup_user(email="revendeur@test.com", api_key="local_key")

#     with app.app_context():
#         Product.query.delete()
#         db.session.commit()

#         product = Product(name="Produit Local Test", description="Backup", price=5.0, stock=1)
#         db.session.add(product)
#         db.session.commit()

#         print("✅ Produit ajouté en BDD :", Product.query.first().name)

#     res = client.get("/api/revendeurs/products", headers={"x-api-key": "local_key"})
#     print("RESPONSE (200) ➤", res.status_code, res.get_data(as_text=True))  # ⬅️ Ajout
#     assert res.status_code == 200
#     assert any(p["name"] == "Produit Local Test" for p in res.get_json())
#     del os.environ["USE_MOCK_PRODUCTS"]








# def test_revendeurs_db_empty_returns_503(client, setup_user, app):
#     os.environ["USE_MOCK_PRODUCTS"] = "false"
#     setup_user(email="revendeur@test.com", api_key="empty_key")

#     with app.app_context():
#         Product.query.delete()
#         db.session.commit()
#         print("🧹 Base nettoyée : aucun produit")
#         assert Product.query.count() == 0

#     res = client.get("/api/revendeurs/products", headers={"x-api-key": "empty_key"})
#     print("RESPONSE (503) ➤", res.status_code, res.get_data(as_text=True))  # ⬅️ Ajout
#     assert res.status_code == 503
#     assert "Aucun produit disponible" in res.get_data(as_text=True)
#     del os.environ["USE_MOCK_PRODUCTS"]










def test_revendeurs_detail_from_db(client, setup_user, app, mocker):
    setup_user(email="revendeur@test.com", api_key="local_key")
    os.environ["USE_MOCK_PRODUCTS"] = "false"

    with app.app_context():
        product = Product(name="Machine DB", description="locale", price=19.0, model_url="model", stock=1, created_at=datetime.utcnow())
        db.session.add(product)
        db.session.commit()
        pid = product.id

    res = client.get(f"/api/revendeurs/products/{pid}", headers={"x-api-key": "local_key"})
    assert res.status_code == 200
    assert res.get_json()["name"] == "Machine DB"

    del os.environ["USE_MOCK_PRODUCTS"]

def test_revendeurs_detail_not_found_in_db(client, setup_user):
    setup_user(email="revendeur@test.com", api_key="missing_key")
    os.environ["USE_MOCK_PRODUCTS"] = "false"

    res = client.get("/api/revendeurs/products/9999", headers={"x-api-key": "missing_key"})
    assert res.status_code == 404

    del os.environ["USE_MOCK_PRODUCTS"]
