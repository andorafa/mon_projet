from app import db
from app.models import User

def test_webshop_valid_key(client):
    # Crée un utilisateur valide avec la bonne clé API
    with client.application.app_context():
        db.create_all()  # Important si pas déjà appelé dans conftest
        db.session.query(User).delete()  # Nettoie les utilisateurs existants
        db.session.add(User(email="test@webshop.com", api_key="webshop123"))
        db.session.commit()

    # Appelle la route protégée avec la clé API correcte
    response = client.get("/api/webshop/products", headers={"x-api-key": "webshop123"})

    # Vérifie que l'accès est autorisé
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert "products" in response.json
