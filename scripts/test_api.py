import os
import time
import requests

# Adresse du backend Flask
#BASE_URL = "http://127.0.0.1:5000"
BASE_URL = "https://payetonkawa-api.onrender.com"


# Variables globales
VALID_API_KEY = None  # Pas défini au départ
INVALID_API_KEY = "cle_invalide"
WEBSHOP_API_KEY = "webshop123"

def test_create_user_success():
    global VALID_API_KEY
    response = requests.post(
        f"{BASE_URL}/api/users",
        json={"email": "testuser@example.com"}
    )
    print(f"Réponse status: {response.status_code}")
    print(f"Réponse body: {response.text}")
    assert response.status_code == 201
    data = response.json()
    VALID_API_KEY = data["api_key"]
    print(f"✅ test_create_user_success PASSED (Nouvelle clé API : {VALID_API_KEY})")
    time.sleep(1)




def test_create_user_missing_email():
    response = requests.post(
        f"{BASE_URL}/api/users",
        json={}
    )
    assert response.status_code == 400
    print("✅ test_create_user_missing_email PASSED")

def test_authenticate_valid_key():
    global VALID_API_KEY
    response = requests.post(
        f"{BASE_URL}/api/revendeurs/authenticate",
        headers={"x-api-key": VALID_API_KEY}
    )
    assert response.status_code == 200
    print("✅ test_authenticate_valid_key PASSED")

def test_authenticate_invalid_key():
    response = requests.post(
        f"{BASE_URL}/api/revendeurs/authenticate",
        headers={"x-api-key": INVALID_API_KEY}
    )
    assert response.status_code == 401
    print("✅ test_authenticate_invalid_key PASSED")

def test_revendeurs_access_products_success():
    global VALID_API_KEY
    response = requests.get(
        f"{BASE_URL}/api/revendeurs/products",
        headers={"x-api-key": VALID_API_KEY}
    )
    assert response.status_code == 200
    print("✅ test_revendeurs_access_products_success PASSED")

def test_revendeurs_access_products_no_key():
    response = requests.get(
        f"{BASE_URL}/api/revendeurs/products"
    )
    assert response.status_code == 401
    print("✅ test_revendeurs_access_products_no_key PASSED")

def test_webshop_access_products_success():
    response = requests.get(
        f"{BASE_URL}/api/webshop/products",
        headers={"x-api-key": WEBSHOP_API_KEY}
    )
    assert response.status_code == 200
    print("✅ test_webshop_access_products_success PASSED")

def test_webshop_access_products_no_key():
    response = requests.get(
        f"{BASE_URL}/api/webshop/products"
    )
    assert response.status_code == 401
    print("✅ test_webshop_access_products_no_key PASSED")

def test_logout_success():
    global VALID_API_KEY
    response = requests.post(
        f"{BASE_URL}/api/logout",
        headers={"x-api-key": VALID_API_KEY}
    )
    assert response.status_code == 200
    print("✅ test_logout_success PASSED")

def test_logout_no_key():
    response = requests.post(
        f"{BASE_URL}/api/logout"
    )
    assert response.status_code == 400
    print("✅ test_logout_no_key PASSED")

if __name__ == "__main__":
    # Lancer tous les tests
    test_create_user_success()
    test_create_user_missing_email()
    test_authenticate_valid_key()
    test_authenticate_invalid_key()
    test_revendeurs_access_products_success()
    test_revendeurs_access_products_no_key()
    test_webshop_access_products_success()
    test_webshop_access_products_no_key()
    test_logout_success()
    test_logout_no_key()
    print("\n🎯 Tous les tests API terminés avec succès.")
