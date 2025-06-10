import pytest
from app import create_app, db
from app.models import User


def test_authenticate_valid_key(client):
    with client.application.app_context():
        # Supprimer si l'utilisateur existe déjà
        User.query.filter_by(email="auth@test.com").delete()
        db.session.commit()

        # Ajouter un utilisateur
        user = User(email="auth@test.com", api_key="valid_key")
        db.session.add(user)
        db.session.commit()

    # Tester l'authentification avec cette clé
    response = client.post("/api/revendeurs/authenticate", headers={"x-api-key": "valid_key"})
    assert response.status_code == 200


def test_authenticate_invalid_key(client):
    response = client.post("/api/revendeurs/authenticate", headers={"x-api-key": "wrong_key"})
    assert response.status_code == 401
