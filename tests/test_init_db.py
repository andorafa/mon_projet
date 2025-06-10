import pytest
from app import create_app, db



def test_init_db(client):
    response = client.post("/api/admin/init-db")
    assert response.status_code == 200
    assert "message" in response.get_json()
