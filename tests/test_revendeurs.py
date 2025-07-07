import pytest
import os

import os
os.environ["USE_MOCK_PRODUCTS"] = "true"


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

# ---------------------------------------------------
# Tests pour les routes revendeurs avec API mockée
# ---------------------------------------------------

def test_revendeur_list_with_valid_key(client, setup_user, mocker):

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

def test_revendeur_detail_with_valid_key(client, setup_user, mocker):

    setup_user(email="revendeur@test.com", api_key="revendeur_key")

    mock_data = {
        "id": "1",
        "name": "Produit Détail",
        "details": {"description": "Desc Détail", "price": "15.0"},
        "stock": 5,
        "createdAt": datetime.strptime("2024-01-01", "%Y-%m-%d")
    }
    mocker.patch(
        "app.resources.revendeurs.requests.get",
        return_value=MockResponse(json_data=mock_data)
    )

    response = client.get("/api/revendeurs/products/1", headers={"x-api-key": "revendeur_key"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Produit Détail"
    assert data["stock"] == 5

def test_revendeurs_get_direct_valid(client, setup_user, mocker):

    setup_user(email="revendeur@test.com", api_key="valid_key")

    mock_data = [
        {
            "id": "1",
            "name": "Produit Test",
            "details": {"description": "Desc", "price": "1.0"},
            "stock": 20,
            "createdAt": datetime.strptime("2024-01-01", "%Y-%m-%d")
        }
    ]
    mocker.patch(
        "app.resources.revendeurs.requests.get",
        return_value=MockResponse(json_data=mock_data)
    )

    res = client.get("/api/revendeurs/products", headers={"x-api-key": "valid_key"})
    assert res.status_code == 200
    data = res.get_json()
    assert data[0]["name"] == "Produit Test"


del os.environ["USE_MOCK_PRODUCTS"]
