import pytest
from app import create_app, db
from app.models import User


def test_create_user(client):
    response = client.post("/api/users", json={"email": "unit@test.com"})
    assert response.status_code == 201
    assert "api_key" in response.get_json()

def test_create_user_missing_email(client):
    response = client.post("/api/users", json={})
    assert response.status_code == 400

def test_existing_user_gets_new_api_key(client):
    with client.application.app_context():
        # Crée un utilisateur existant
        user = User(email="regen@test.com", api_key="old_key")
        db.session.add(user)
        db.session.commit()

    # Appel de l'API avec même email
    response = client.post("/api/users", json={"email": "regen@test.com"})
    assert response.status_code == 201
    new_key = response.get_json()["api_key"]
    assert new_key != "old_key"  # La clé a bien été régénérée
