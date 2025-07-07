
import os
os.environ["USE_MOCK_PRODUCTS"] = "true"

import pytest
import requests
from app import db
from app.models import Product
from datetime import datetime


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")

# -------------------------------
# Tests CRM API
# -------------------------------

def test_get_crm_customers(client, mocker):
    mock_data = [{
        "id": "1", "name": "Alice", "firstName": "Alice", "lastName": "Dupont",
        "address": {"city": "Paris", "postalCode": "75000"},
    }]
    mocker.patch("app.resources.crm_api.requests.get", return_value=MockResponse(mock_data))
    response = client.get("/api/crm/customers")
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["name"] == "Alice"

def test_get_crm_orders_by_customer(client, mocker):
    mock_data = {"id": "1", "orders": [{"id": "101", "products": [{"id": "1", "name": "Café"}]}]}
    mocker.patch("app.resources.crm_api.requests.get", return_value=MockResponse(mock_data))
    response = client.get("/api/crm/customers/1/orders")
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["id"] == "101"

def test_get_crm_products_by_order(client, mocker):
    mock_data = {"id": "1", "orders": [{"id": "101", "products": [{"id": "1", "name": "Café"}]}]}
    mocker.patch("app.resources.crm_api.requests.get", return_value=MockResponse(mock_data))
    response = client.get("/api/crm/customers/1/orders/101/products")
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["name"] == "Café"

def test_crm_api_unavailable(client, mocker):
    mocker.patch("app.resources.crm_api.requests.get", side_effect=requests.exceptions.ConnectionError("API down"))
    response = client.get("/api/crm/customers")
    assert response.status_code == 503
    assert "API mock hors ligne" in response.get_data(as_text=True)

def test_crm_customer_not_found(client, mocker):
    mocker.patch("app.resources.crm_api.requests.get", return_value=MockResponse({}, status_code=404))
    response = client.get("/api/crm/customers/999/orders")
    assert response.status_code == 404
    assert "Client 999 introuvable" in response.get_data(as_text=True)

# -------------------------------
# Tests ERP API
# -------------------------------

def test_get_erp_products(client, mocker):
    mock_data = [{
        "id": "1", "name": "Café Moka",
        "details": {"description": "Doux", "price": "5.5"},
        "stock": 100,
        "createdAt": datetime.strptime("2024-01-01", "%Y-%m-%d")
    }]
    mocker.patch("app.resources.erp_api.requests.get", return_value=MockResponse(mock_data))
    response = client.get("/api/erp/products")
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["name"] == "Café Moka"

def test_get_erp_product_detail_valid(client, mocker):
    mock_data = {
        "id": "1", "name": "Café Moka",
        "details": {"description": "Doux", "price": "5.5"},
        "stock": 100, "createdAt": datetime.strptime("2024-01-01", "%Y-%m-%d")
    }
    mocker.patch("app.resources.erp_api.requests.get", return_value=MockResponse(mock_data))
    response = client.get("/api/erp/products/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Café Moka"

def test_get_erp_product_detail_not_found(client, mocker):
    mocker.patch("app.resources.erp_api.requests.get", return_value=MockResponse({}, status_code=404))
    response = client.get("/api/erp/products/999")
    assert response.status_code == 404
    response_json = response.get_json()
    assert "Produit 999" in response_json["message"]
    assert "non trouvé" in response_json["message"]

def test_erp_api_unavailable_with_fallback(client, mocker):
    mocker.patch("app.resources.erp_api.requests.get", side_effect=requests.exceptions.ConnectionError("API down"))
    
    # Nettoyer base locale
    Product.query.delete()
    db.session.commit()
    
    product = Product(
        name="Produit BDD",
        description="local",
        price=10.0,
        stock=5,
        created_at=datetime.strptime("2024-01-01", "%Y-%m-%d")
    )
    db.session.add(product)
    db.session.commit()
    response = client.get("/api/erp/products")
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["name"] == "Produit BDD"

def test_erp_api_unavailable_no_fallback(client, mocker):
    mocker.patch("app.resources.erp_api.requests.get", side_effect=requests.exceptions.ConnectionError("API down"))
    Product.query.delete()
    db.session.commit()
    response = client.get("/api/erp/products")
    assert response.status_code == 503
    response_json = response.get_json()
    assert "Aucune donnée disponible" in response_json["message"]


del os.environ["USE_MOCK_PRODUCTS"]
