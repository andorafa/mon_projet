import pytest
from app import db
from app.models import User, Product

# 🔒 Tests /api/revendeurs/logout
def test_logout_valid_key(client):
    with client.application.app_context():
        # Vérifie si l'utilisateur existe déjà
        existing_user = User.query.filter_by(email="logout@test.com").first()
        if not existing_user:
            user = User(email="logout@test.com", api_key="logout123")
            db.session.add(user)
        else:
            existing_user.api_key = "logout123"
        db.session.commit()

    response = client.post("/api/revendeurs/logout", headers={"x-api-key": "logout123"})
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Déconnexion réussie"

def test_logout_missing_key(client):
    res = client.post("/api/revendeurs/logout")
    assert res.status_code == 400

def test_logout_invalid_key(client):
    res = client.post("/api/revendeurs/logout", headers={"x-api-key": "invalid"})
    assert res.status_code == 401

# 👤 Tests /api/users
def test_user_creation_missing_email(client):
    res = client.post("/api/users", json={})
    assert res.status_code == 400

def test_user_creation_existing_user(client):
    email = "existing@test.com"
    res1 = client.post("/api/users", json={"email": email})
    key1 = res1.get_json()["api_key"]

    res2 = client.post("/api/users", json={"email": email})
    key2 = res2.get_json()["api_key"]

    assert key1 != key2

# 🛍️ Tests /api/webshop/products
def test_webshop_invalid_key(client):
    res = client.get("/api/webshop/products", headers={"x-api-key": "invalid"})
    assert res.status_code == 401

# 📦 Tests /api/products/<id>
def test_product_not_found(client):
    res = client.get("/api/products/999999")
    assert res.status_code == 404

# ⚙️ Tests /api/admin/init-db
def test_init_db(client):
    res = client.post("/api/admin/init-db")
    assert res.status_code == 200
    assert "Base de données" in res.get_json()["message"]
