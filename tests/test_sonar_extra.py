import os
import pytest
from app import db
from app.models import User, Product

def create_user(client, email, key):
    with client.application.app_context():
        # 🔧 Ajouté : suppression si l'utilisateur existe déjà
        db.session.query(User).filter_by(email=email).delete()
        db.session.commit()

        db.session.add(User(email=email, api_key=key))
        db.session.commit()


def create_product(client):
    with client.application.app_context():
        db.session.add(Product(name="Test", description="test", price=5.0, model_url="url"))
        db.session.commit()

def test_revendeurs_products(client):
    #os.environ["USE_MOCK_PRODUCTS"] = "true"  # ✅ ajout

    create_user(client, "test@coverage.com", "key123")
    create_product(client)
    res = client.get("/api/revendeurs/products", headers={"x-api-key": "key123"})
    assert res.status_code == 200

    #del os.environ["USE_MOCK_PRODUCTS"]  # ✅ nettoyage

def test_authenticate_success(client):
    with client.application.app_context():
        db.session.query(User).filter_by(email="auth@test.com").delete()
        db.session.commit()
        db.session.add(User(email="auth@test.com", api_key="authkey"))
        db.session.commit()

    res = client.post("/api/revendeurs/authenticate", headers={"x-api-key": "authkey"})
    assert res.status_code == 200


def test_logout_success(client):
    with client.application.app_context():
        db.session.query(User).filter_by(email="logout@test.com").delete()
        db.session.commit()
        db.session.add(User(email="logout@test.com", api_key="logoutkey"))
        db.session.commit()

    res = client.post("/api/revendeurs/logout", headers={"x-api-key": "logoutkey"})
    assert res.status_code == 200


def test_user_creation(client):
    res = client.post("/api/users", json={"email": "newuser@test.com",
    "first_name": "New",
    "last_name": "User"})
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
    with client.application.app_context():
        db.session.query(User).filter_by(api_key="webshop123").delete()
        db.session.commit()
        db.session.add(User(email="webshop@client.com", api_key="webshop123"))
        db.session.commit()

    res = client.get("/api/webshop/products", headers={"x-api-key": "webshop123"})
    assert res.status_code == 200


def test_init_db(client):
    res = client.post("/api/admin/init-db")
    assert res.status_code == 200
