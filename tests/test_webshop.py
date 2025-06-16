from app import db
from app.models import Product

def test_webshop_valid_key(client, setup_user):
    with client.application.app_context():
        Product.query.delete()
        db.session.add(Product(
            name="Produit Test",
            description="Un café sympa",
            price=4.2,
            model_url="http://test.url"
        ))
        db.session.commit()

    response = client.get("/api/webshop/products", headers={"x-api-key": "webshop123"})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(p["name"] == "Produit Test" for p in data)

def test_webshop_missing_key(client):
    response = client.get("/api/webshop/products")
    assert response.status_code == 401
