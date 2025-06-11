import requests # type: ignore

# 🛠️ L'URL d'API Flask
BASE_URL = "http://127.0.0.1:5000"

# Remplacer par l'email que je veux utiliser pour créer l'utilisateur
email_to_register = "testuser@example.com"

def create_user():
    url = f"{BASE_URL}/api/users"
    payload = {"email": email_to_register}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            data = response.json()
            print("✅ Utilisateur créé avec succès !")
            print(f"Clé API générée : {data['api_key']}")
            print(f"QR Code (base64) : {data['qr_code'][:50]}...")  # on affiche seulement le début du QR code base64
        else:
            print(f"❌ Erreur ({response.status_code}) : {response.text}")
    except Exception as e:
        print(f"Erreur de connexion : {e}")

if __name__ == "__main__":
    create_user()