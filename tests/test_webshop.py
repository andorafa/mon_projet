import os
import pytest
import requests
from datetime import datetime
from app.config import Config
from app.models import Product, OrderProduct
from app import db

headers = {"x-api-key": Config.API_WEBSHOP_KEY}


class MockResponse:
    def __init__(self, json_data=None, status_code=200):
        self._json_data = json_data or {}
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


# -------------------------------
# Tests Webshop API
# -------------------------------

def test_webshop_get_products_with_valid_key(client, mocker):
    os.environ["USE_MOCK_PRODUCTS"] = "true"

    mock_data = [{
        "id": "1",
        "name": "Produit Webshop",
        "details": {"description": "Test", "price": "12.5"},
        "stock": 10,
        "createdAt": "2024-01-01"
    }]

    mocker.patch("app.resources.webshop.requests.get", return_value=MockResponse(mock_data))

    res = client.get("/api/webshop/products", headers=headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data[0]["name"] == "Produit Webshop"

    del os.environ["USE_MOCK_PRODUCTS"]


def test_webshop_get_product_detail_valid(client, mocker):
    os.environ["USE_MOCK_PRODUCTS"] = "true"

    mock_data = {
        "id": "1",
        "name": "Produit Webshop",
        "details": {"description": "Desc", "price": "9.99"},
        "stock": 20,
        "createdAt": "2024-01-01"
    }

    mocker.patch("app.resources.webshop.requests.get", return_value=MockResponse(mock_data))

    res = client.get("/api/webshop/products/1", headers=headers)
    assert res.status_code == 200
    assert res.get_json()["price"] == 9.99

    del os.environ["USE_MOCK_PRODUCTS"]


def test_webshop_get_product_detail_not_found_in_mock(client, mocker):
    os.environ["USE_MOCK_PRODUCTS"] = "true"

    mocker.patch("app.resources.webshop.requests.get", return_value=MockResponse({}, status_code=404))

    res = client.get("/api/webshop/products/999", headers=headers)
    assert res.status_code == 404
    assert "introuvable" in res.get_data(as_text=True)

    del os.environ["USE_MOCK_PRODUCTS"]


def test_webshop_get_product_unauthorized(client):
    res = client.get("/api/webshop/products")
    assert res.status_code == 401


def test_webshop_get_product_invalid_key(client):
    res = client.get("/api/webshop/products", headers={"x-api-key": "wrong_key"})
    assert res.status_code == 401


def test_webshop_product_detail_not_found_in_db(client, mocker):
    os.environ["USE_MOCK_PRODUCTS"] = "false"
    mocker.patch("app.resources.webshop.requests.get", side_effect=requests.RequestException("API down"))

    res = client.get("/api/webshop/products/9999", headers=headers)
    assert res.status_code == 404

    del os.environ["USE_MOCK_PRODUCTS"]


def test_webshop_fallback_on_mock_failure(client, mocker, app):
    os.environ["USE_MOCK_PRODUCTS"] = "true"

    mocker.patch("app.resources.webshop.requests.get", side_effect=requests.RequestException("API down"))

    with app.app_context():


        # Supprimer les relations d'abord
        db.session.query(OrderProduct).delete()
        db.session.commit()

        # Puis supprimer les produits
        db.session.query(Product).delete()
        db.session.commit()

        # Ajout d'un produit local pour fallback
        product = Product(
            name="Produit Local",
            description="Backup",
            price=5.0,
            stock=1,
            created_at=datetime.strptime("2024-01-01", "%Y-%m-%d"),
            model_url=""
        )
        db.session.add(product)
        db.session.commit()


    res = client.get("/api/webshop/products", headers=headers)

    print(">>> STATUS:", res.status_code)
    print(">>> BODY:", res.get_json())

    assert res.status_code == 200
    assert res.get_json()[0]["name"] == "Produit Local"

    del os.environ["USE_MOCK_PRODUCTS"]






def test_webshop_fallback_no_products(client, mocker, app):
    os.environ["USE_MOCK_PRODUCTS"] = "true"

    mocker.patch("app.resources.webshop.requests.get", side_effect=requests.RequestException("API down"))

    with app.app_context():
        from app.models import Product
        from app import db
        Product.query.delete()
        db.session.commit()
        assert Product.query.count() == 0

    res = client.get("/api/webshop/products", headers=headers)

    print("\nRESPONSE STATUS:", res.status_code)
    print("RESPONSE BODY:", res.get_json())

    assert res.status_code == 503
    assert "Aucune donnée disponible" in res.get_json()["message"]

    del os.environ["USE_MOCK_PRODUCTS"]



