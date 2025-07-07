import os
import pytest
from datetime import datetime
from app import db
from app.models import User, Product

# ---------------------------------------------------
# MOCK HTTP
# ---------------------------------------------------

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

# ---------------------------------------------------
# TEST DIRECT REVENDEURS (avec mock ERP actif)
# ---------------------------------------------------

def test_revendeurs_get_direct_valid(client, setup_user, mocker):
    os.environ["USE_MOCK_PRODUCTS"] = "true"

    setup_user(email="revendeur@test.com", api_key="valid_key")
    mock_data = [
        {
            "id": "1",
            "name": "Produit Test",
            "details": {"description": "Desc", "price": "1.0"},
            "stock": 20,
            "createdAt": datetime.strptime("2024-01-01", "%Y-%m-%d")
        }
    ]
    mocker.patch("app.resources.revendeurs.requests.get", return_value=MockResponse(mock_data))
    res = client.get("/api/revendeurs/products", headers={"x-api-key": "valid_key"})
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert data[0]["name"] == "Produit Test"

    del os.environ["USE_MOCK_PRODUCTS"]

# ---------------------------------------------------
# TESTS ERREURS & AUTHENTIFICATION
# ---------------------------------------------------

def test_revendeurs_get_direct_missing_key(client):
    res = client.get("/api/revendeurs/products")
    assert res.status_code == 401

def test_revendeurs_get_direct_invalid_key(client):
    res = client.get("/api/revendeurs/products", headers={"x-api-key": "wrong"})
    assert res.status_code == 401

def test_authenticate_post_valid(client, setup_user):
    setup_user(email="auth@test.com", api_key="authkey")
    response = client.post("/api/revendeurs/authenticate", headers={"x-api-key": "authkey"})
    assert response.status_code == 200

def test_authenticate_post_missing_key(client):
    res = client.post("/api/revendeurs/authenticate")
    assert res.status_code == 400

def test_authenticate_post_invalid_key(client):
    res = client.post("/api/revendeurs/authenticate", headers={"x-api-key": "invalid"})
    assert res.status_code == 401
