from app import db
from app.config import Config

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

def test_webshop_valid_key(client, mocker):
    mock_data = [
        {
            "id": "1",
            "name": "Produit Shop",
            "details": {"description": "Desc", "price": "8.0"},
            "stock": 20,
            "createdAt": "2024-06-01"
        }
    ]
    mocker.patch(
        "app.resources.webshop.requests.get",
        return_value=MockResponse(json_data=mock_data)
    )
    response = client.get("/api/webshop/products", headers={"x-api-key": Config.API_WEBSHOP_KEY})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["name"] == "Produit Shop"

def test_webshop_missing_key(client):
    response = client.get("/api/webshop/products")
    assert response.status_code == 401

def test_webshop_invalid_key(client):
    response = client.get("/api/webshop/products", headers={"x-api-key": "wrong_key"})
    assert response.status_code == 401
