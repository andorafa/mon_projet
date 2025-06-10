import pytest
from app import create_app, db
from app.models import User



def test_create_user_route(client):
    response = client.post("/api/users", json={"email": "unittest@example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "api_key" in data
    assert data["api_key"]
