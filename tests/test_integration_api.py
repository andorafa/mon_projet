import pytest
from app import db
from app.models import Product

# ✅ Test inscription d'utilisateur (POST /api/users)
def test_user_creation(client):
    response = client.post("/api/users", json={"email": "integration@test.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "api_key" in data
    assert isinstance(data["api_key"], str)

# ✅ Test authentification avec clé générée
def test_authentication_flow(client):
    # Créer un utilisateur
    res = client.post("/api/users", json={"email": "flow@test.com"})
    assert res.status_code == 201
    api_key = res.get_json()["api_key"]

    # Authentifier
    res = client.post("/api/revendeurs/authenticate", headers={"x-api-key": api_key})
    assert res.status_code == 200
    assert "message" in res.get_json()

# ✅ Test accès protégé sans clé
def test_auth_protected_route_no_key(client):
    res = client.get("/api/revendeurs/products")
    assert res.status_code == 401

# ✅ Test produit : ajout + accès à /api/products/<id>
def test_product_detail_integration(client):
    with client.application.app_context():
        product = Product(name="Machine Test", description="Desc", price=99.99, model_url="model.glb")
        db.session.add(product)
        db.session.commit()
        pid = product.id

    res = client.get(f"/api/products/{pid}")
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["name"] == "Machine Test"
    assert json_data["price"] == 99.99

# ✅ Test 404 produit non trouvé
def test_product_not_found(client):
    res = client.get("/api/products/999999")
    assert res.status_code == 404
