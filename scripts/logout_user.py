import os
import sys
import requests # type: ignore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 🛠️ L'URL de l'API Flask
BASE_URL = "http://127.0.0.1:5000"

# 🔑 Remplacer par la clé API de l'utilisateur que je veux déconnecter
api_key_to_logout = "La_vraie_cle_API_revendeur"

def logout_user():
    url = f"{BASE_URL}/api/revendeurs/logout"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key_to_logout
    }

    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print("✅ Déconnexion réussie !")
        else:
            print(f"❌ Erreur ({response.status_code}) : {response.text}")
    except Exception as e:
        print(f"Erreur de connexion : {e}")

if __name__ == "__main__":
    logout_user()
