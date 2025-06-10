def test_webshop_valid_key(client, setup_user):
    response = client.get("/api/webshop/products", headers={"x-api-key": "webshop123"})
    assert response.status_code == 200
    assert "products" in response.get_json()

def test_webshop_missing_key(client):
    response = client.get("/api/webshop/products")
    assert response.status_code == 401
