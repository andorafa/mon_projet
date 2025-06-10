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
