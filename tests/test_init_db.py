def test_init_db(client):
    response = client.post("/api/admin/init-db")
    assert response.status_code == 200
    assert "message" in response.get_json()

def test_init_db_route(client):
    res = client.post("/api/admin/init-db")
    assert res.status_code == 200
    assert "message" in res.get_json()
