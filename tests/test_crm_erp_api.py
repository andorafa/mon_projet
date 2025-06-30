from app import db
import pytest

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

def test_get_crm_customers(client, mocker):
    mock_data = [
        {
            "id": "1",
            "name": "Alice",
            "firstName": "Alice",
            "lastName": "Dupont",
            "address": {"city": "Paris", "postalCode": "75000"},
        }
    ]
    mocker.patch(
        "app.resources.crm_api.requests.get",
        return_value=MockResponse(json_data=mock_data)
    )
    response = client.get("/api/crm/customers")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["name"] == "Alice"

def test_get_crm_orders_by_customer(client, mocker):
    mock_data = {
        "id": "1",
        "orders": [
            {"id": "101", "date": "2024-05-01", "products": [{"id": "1", "name": "Café"}]}
        ]
    }
    mocker.patch(
        "app.resources.crm_api.requests.get",
        return_value=MockResponse(json_data=mock_data)
    )
    response = client.get("/api/crm/customers/1/orders")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["id"] == "101"

def test_get_crm_products_by_order(client, mocker):
    mock_data = {
        "id": "1",
        "orders": [
            {"id": "101", "products": [{"id": "1", "name": "Café"}]}
        ]
    }
    mocker.patch(
        "app.resources.crm_api.requests.get",
        return_value=MockResponse(json_data=mock_data)
    )
    response = client.get("/api/crm/customers/1/orders/101/products")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["name"] == "Café"

def test_get_erp_products(client, mocker):
    mock_data = [
        {
            "id": "1",
            "name": "Café Moka",
            "details": {"description": "Doux", "price": "5.5"},
            "stock": 100,
            "createdAt": "2024-06-01"
        }
    ]
    mocker.patch(
        "app.resources.erp_api.requests.get",
        return_value=MockResponse(json_data=mock_data)
    )
    response = client.get("/api/erp/products")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["name"] == "Café Moka"

def test_get_erp_product_detail_valid(client, mocker):
    mock_data = {
        "id": "1",
        "name": "Café Moka",
        "details": {"description": "Doux", "price": "5.5"},
        "stock": 100,
        "createdAt": "2024-06-01"
    }
    mocker.patch(
        "app.resources.erp_api.requests.get",
        return_value=MockResponse(json_data=mock_data)
    )
    response = client.get("/api/erp/products/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Café Moka"
    assert data["price"] == 5.5

def test_get_erp_product_detail_not_found(client, mocker):
    mocker.patch(
        "app.resources.erp_api.requests.get",
        return_value=MockResponse(json_data={}, status_code=404)
    )
    response = client.get("/api/erp/products/999")
    assert response.status_code == 404
