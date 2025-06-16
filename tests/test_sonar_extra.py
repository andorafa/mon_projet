import pytest
from app import db
from app.models import User, Product

def create_user(client, email, key):
    with client.application.app_context():
        db.session.add(User(email=email, api_key=key))
        db.session.commit()

def create_product(client):
    with client.application.app_context():
        db.session.add(Product(name="Test", description="test", price=5.0, model_url="url"))
        db.session.commit()

def test_revendeurs_products(client):
    create_user(client, "test@coverage.com", "key123")
    create_product(client)
    res = client.get("/api/revendeurs/products", headers={"x-api-key": "key123"})
    assert res.status_code == 200

def test_authenticate_success(client):
    create_user(client, "auth@test.com", "authkey")
    res = client.post("/api/revendeurs/authenticate", headers={"x-api-key": "authkey"})
    assert res.status_code == 200

def test_logout_success(client):
    create_user(client, "logout@test.com", "logoutkey")
    res = client.post("/api/logout", headers={"x-api-key": "logoutkey"})
    assert res.status_code == 200

def test_user_creation(client):
    res = client.post("/api/users", json={"email": "newuser@test.com"})
    assert res.status_code == 201
    assert "api_key" in res.get_json()

def test_product_detail_found(client):
    with client.application.app_context():
        p = Product(name="Machine", description="desc", price=10.0, model_url="")
        db.session.add(p)
        db.session.commit()
        pid = p.id
    res = client.get(f"/api/products/{pid}")
    assert res.status_code == 200

def test_product_detail_not_found(client):
    res = client.get("/api/products/999999")
    assert res.status_code == 404

def test_webshop_access(client):
    create_user(client, "webshop@client.com", "webshop123")
    create_product(client)
    res = client.get("/api/webshop/products", headers={"x-api-key": "webshop123"})
    assert res.status_code == 200

def test_init_db(client):
    res = client.post("/api/admin/init-db")
    assert res.status_code == 200
