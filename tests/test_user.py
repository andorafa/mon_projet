from app import db
from app.models import User

def test_create_user(client):
    response = client.post("/api/users", json={
        "email": "unit@test.com",
        "first_name": "Unit",
        "last_name": "Test"
    })
    assert response.status_code == 201
    assert "api_key" in response.get_json()

def test_create_user_missing_email(client):
    response = client.post("/api/users", json={})
    assert response.status_code == 400

def test_existing_user_gets_new_api_key(client):
    email = "regen@test.com"

    with client.application.app_context():
        # Supprime les anciens utilisateurs si existants
        User.query.filter_by(email=email).delete()
        db.session.commit()

        user = User(email=email, api_key="old_key")
        db.session.add(user)
        db.session.commit()

    response = client.post("/api/users", json={
        "email": email,
        "first_name": "Jean",
        "last_name": "Dupont"
    })
    assert response.status_code == 201
    new_key = response.get_json()["api_key"]
    assert new_key != "old_key"

    with client.application.app_context():
        updated_user = User.query.filter_by(email=email).first()
        assert updated_user.api_key == new_key
        assert updated_user.first_name == "Jean"
        assert updated_user.last_name == "Dupont"


def test_create_user_and_check_qr_code(client):
    email = "coveragetest@example.com"
    response = client.post("/api/users", json={
        "email": email,
        "first_name": "Coverage",
        "last_name": "Test"
    })
    assert response.status_code == 201
    json_data = response.get_json()
    assert "api_key" in json_data
    assert "qr_code" in json_data
