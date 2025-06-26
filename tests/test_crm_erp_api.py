def test_get_crm_customers(client):
    response = client.get("/api/crm/customers")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any("name" in c for c in data)

def test_get_crm_orders_by_customer(client):
    response = client.get("/api/crm/customers/1/orders")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all("customerId" in o for o in data)

def test_get_crm_products_by_order(client):
    response = client.get("/api/crm/customers/1/orders/101/products")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all("name" in p for p in data)


def test_get_erp_products(client):
    response = client.get("/api/erp/products")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all("price" in p for p in data)

def test_get_erp_product_detail_valid(client):
    response = client.get("/api/erp/products/1")
    assert response.status_code == 200
    data = response.get_json()
    assert "name" in data
    assert "description" in data

def test_get_erp_product_detail_not_found(client):
    response = client.get("/api/erp/products/999")
    assert response.status_code == 404
