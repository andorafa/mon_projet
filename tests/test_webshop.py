import pytest
from app import create_app, db
from app.config import Config
from app.models import User


def test_webshop_valid_key(client):
    with client.application.app_context():
        # Crée un utilisateur avec la bonne clé
        db.session.add(User(email="test@webshop.com", api_key="webshop123"))
        db.session.commit()

    response = client.get("/api/webshop/products", headers={"x-api-key": "webshop123"})
    assert response.status_code == 200

def test_webshop_missing_key(client):
    response = client.get("/api/webshop/products")
    assert response.status_code == 401
