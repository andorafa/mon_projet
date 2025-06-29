# app/mock_data/mock_crm_data.py

customers = [
    {"id": "1", "name": "Alice"},
    {"id": "2", "name": "Bob"},
]

orders_by_customer = {
    "1": [{"id": "101", "customerId": "1", "date": "2024-05-01"}],
    "2": [{"id": "102", "customerId": "2", "date": "2024-06-01"}],
}

products_by_order = {
    "101": [{"id": "1", "name": "Café Moka", "price": 5.5}],
    "102": [{"id": "2", "name": "Thé Vert", "price": 3.0}],
}
