from app import db
from app.models import Product

def test_product_detail(client):
    with client.application.app_context():
        product = Product(name="Café Test", description="Description test", price=15.0, model_url="url_test")
        db.session.add(product)
        db.session.commit()
        product_id = product.id

    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Café Test"

def test_product_detail_not_found(client):
    response = client.get("/api/products/9999")
    assert response.status_code == 404
