def test_create_user_route(client):
    response = client.post("/api/users", json={"email": "unittest@example.com",
    "first_name": "Unit",
    "last_name": "Test"})
    assert response.status_code == 201
    data = response.get_json()
    assert "api_key" in data
    assert data["api_key"]
