import pytest
from app import db
from app.models import Product, User

# 🔁 Test pour /api/admin/init-db
def test_admin_init_db(client):
    res = client.post("/api/admin/init-db")
    assert res.status_code == 200
    assert "message" in res.get_json()

# 🔎 Test /api/products/<id> avec produit existant
def test_product_detail_found(client):
    with client.application.app_context():
        product = Product(name="Produit Testé", description="desc", price=9.99, model_url="url")
        db.session.add(product)
        db.session.commit()
        pid = product.id

    res = client.get(f"/api/products/{pid}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["name"] == "Produit Testé"

# ❌ Test /api/products/<id> non trouvé
def test_product_detail_not_found(client):
    res = client.get("/api/products/999999")
    assert res.status_code == 404

# 🛍️ Test webshop avec clé correcte
def test_webshop_valid_key(client):
    with client.application.app_context():
        user = User(email="webshop@test.com", api_key="webshop123")
        db.session.add(user)
        db.session.commit()

    res = client.get("/api/webshop/products", headers={"x-api-key": "webshop123"})
    assert res.status_code == 200
    assert isinstance(res.get_json(), list) or "products" in res.get_json()

# 🧨 Test webshop sans clé
def test_webshop_missing_key(client):
    res = client.get("/api/webshop/products")
    assert res.status_code == 401

# 🔁 Test logout avec utilisateur connu
def test_logout_valid(client):
    with client.application.app_context():
        user = User(email="logout@test.com", api_key="logout123")
        db.session.add(user)
        db.session.commit()

    res = client.post("/api/revendeurs/logout", headers={"x-api-key": "logout123"})
    assert res.status_code == 200
    assert "message" in res.get_json()

# 🧨 Test logout avec clé invalide
def test_logout_invalid(client):
    res = client.post("/api/revendeurs/logout", headers={"x-api-key": "wrong"})
    assert res.status_code == 401
