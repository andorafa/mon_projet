from app import db
from app.models import User

def test_revendeur_access_with_valid_key(client):
    with client.application.app_context():
        User.query.filter_by(email="revendeur@test.com").delete()
        db.session.commit()
        db.session.add(User(email="revendeur@test.com", api_key="revendeur_key"))
        db.session.commit()

    response = client.get("/api/revendeurs/products", headers={"x-api-key": "revendeur_key"})
    assert response.status_code == 200

def test_revendeur_access_no_key(client):
    response = client.get("/api/revendeurs/products")
    assert response.status_code == 401

def test_authenticate_valid_key(client):
    from app.models import User
    with client.application.app_context():
        user = User(email="authcov@test.com", api_key="auth123")
        db.session.add(user)
        db.session.commit()

    res = client.post("/api/revendeurs/authenticate", headers={"x-api-key": "auth123"})
    assert res.status_code == 200

def test_revendeurs_products_list(client):
    from app.models import Product, User
    with client.application.app_context():
        db.session.add(User(email="revendeurcov@test.com", api_key="revkey123"))
        db.session.add(Product(name="Test Produit", description="Desc", price=10.0, model_url=""))
        db.session.commit()

    res = client.get("/api/revendeurs/products", headers={"x-api-key": "revkey123"})
    assert res.status_code == 200

def test_revendeurs_logout(client):
    from app.models import User
    with client.application.app_context():
        db.session.add(User(email="logoutcov@test.com", api_key="logoutkey123"))
        db.session.commit()

    res = client.post("/api/revendeurs/logout", headers={"x-api-key": "logoutkey123"})
    assert res.status_code == 200
