from app import db
from app.models import Product
import pytest
from datetime import datetime


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

def test_product_detail(client, mocker):
    # Nettoyer la BDD locale avant le test
    with client.application.app_context():
        product = db.session.get(Product, 99999)
        if product:
            db.session.delete(product)
            db.session.commit()

    mock_data = {
        "id": "99999",
        "name": "Café Test",
        "details": {"description": "Desc Test", "price": "15.0"},
        "stock": 50,
        "createdAt": datetime.strptime("2024-01-01", "%Y-%m-%d")
    }
    mocker.patch(
        "app.resources.product_detail.requests.get",
        return_value=MockResponse(json_data=mock_data)
    )
    response = client.get("/api/products/99999")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Café Test"
    assert data["price"] == 15.0

def test_product_detail_not_found(client, mocker):
    mocker.patch(
        "app.resources.product_detail.requests.get",
        return_value=MockResponse(json_data={}, status_code=404)
    )
    response = client.get("/api/products/9999")
    assert response.status_code == 404
