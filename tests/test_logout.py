from app import db
from app.models import User

def test_logout_valid_key(client):
    with client.application.app_context():
        User.query.filter_by(email="logout@test.com").delete()
        db.session.commit()
        db.session.add(User(email="logout@test.com", api_key="logout_key"))
        db.session.commit()

    response = client.post("/api/logout", headers={"x-api-key": "logout_key"})
    assert response.status_code == 200

def test_logout_missing_key(client):
    response = client.post("/api/logout")
    assert response.status_code == 400
