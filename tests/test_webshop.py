import pytest
from app import db
from app.models import Product


def test_webshop_valid_key(client, setup_user):
    with client.application.app_context():
        # 🔁 Nettoyer la table Product pour éviter l'accumulation
        Product.query.delete()

        # ✅ Ajouter un seul produit de test
        db.session.add(Product(
            name="Produit Test",
            description="Un café sympa",
            price=4.2,
            model_url="http://test.url"
        ))
        db.session.commit()

    # 🧪 Appel de l'API avec la bonne clé
    response = client.get("/api/webshop/products", headers={"x-api-key": "webshop123"})
    assert response.status_code == 200
    data = response.get_json()
    assert "products" in data
    assert len(data["products"]) == 1
    assert data["products"][0]["name"] == "Produit Test"


def test_webshop_missing_key(client):
    # 🚫 Pas de clé envoyée
    response = client.get("/api/webshop/products")
    assert response.status_code == 401
