# tests/test_direct_revendeurs.py

import pytest
from app import db
from app.models import User, Product
from tests.conftest import setup_user

# def setup_user(api_key="valid_key", email="user@example.com"):
#     user = User(email=email, api_key=api_key)
#     db.session.add(user)
#     db.session.commit()
#     return user

def test_revendeurs_get_direct_valid(client, setup_user):
    setup_user(api_key="valid_key", email="revendeur@test.com")

    db.session.add(Product(name="Test", description="desc", price=1.0, model_url=""))
    db.session.commit()

    res = client.get("/api/revendeurs/products", headers={"x-api-key": "valid_key"})
    assert res.status_code == 200
    assert isinstance(res.get_json(), list) or "products" in res.get_json()

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
