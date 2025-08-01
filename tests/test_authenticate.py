from app import db
from app.models import User

def test_authenticate_valid_key(client):
    with client.application.app_context():
        User.query.filter_by(email="auth@test.com").delete()
        db.session.commit()

        user = User(email="auth@test.com", api_key="auth_key_123")
        db.session.add(user)
        db.session.commit()

        res = client.post("/api/revendeurs/authenticate", headers={"x-api-key": "auth_key_123"})
        assert res.status_code == 200


def test_authenticate_invalid_key(client):
    response = client.post("/api/revendeurs/authenticate", headers={"x-api-key": "wrong_key"})
    assert response.status_code == 401
