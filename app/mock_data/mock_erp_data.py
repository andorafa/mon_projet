# app/mock_data/mock_erp_data.py

# products = [
#     {"id": "1", "name": "Café Moka", "description": "Doux et fruité", "price": 5.5},
#     {"id": "2", "name": "Thé Vert", "description": "Thé bio", "price": 3.0},
# ]


import requests

def get_mock_products():
    url = "https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products"
    response = requests.get(url)
    return response.json()
