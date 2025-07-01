from app import db
from app.models import User
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

def test_revendeur_access_with_valid_key(client, setup_user, mocker):
    setup_user(email="revendeur@test.com", api_key="revendeur_key")

    mock_data = [
        {
            "id": "1",
            "name": "Produit Revendeur",
            "details": {"description": "Desc", "price": "5.0"},
            "stock": 10,
            "createdAt": datetime.strptime("2024-01-01", "%Y-%m-%d")
        }
    ]
    mocker.patch(
        "app.resources.revendeurs.requests.get",
        return_value=MockResponse(json_data=mock_data)
    )

    response = client.get("/api/revendeurs/products", headers={"x-api-key": "revendeur_key"})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["name"] == "Produit Revendeur"

def test_revendeur_access_no_key(client):
    response = client.get("/api/revendeurs/products")
    assert response.status_code == 401

def test_revendeur_access_invalid_key(client):
    response = client.get("/api/revendeurs/products", headers={"x-api-key": "wrong_key"})
    assert response.status_code == 401
