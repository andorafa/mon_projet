from app import db
from app.models import User

def test_logout_valid_key(client):
    with client.application.app_context():
        User.query.filter_by(email="logout@test.com").delete()
        db.session.commit()
        db.session.add(User(email="logout@test.com", api_key="logout_key"))
        db.session.commit()

    response = client.post("/api/revendeurs/logout", headers={"x-api-key": "logout_key"})
    assert response.status_code == 200
    assert "message" in response.get_json()

def test_logout_missing_key(client):
    response = client.post("/api/revendeurs/logout")
    assert response.status_code == 400
