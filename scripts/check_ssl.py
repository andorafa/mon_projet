# scripts/check_ssl.py
import os
import psycopg2
from urllib.parse import urlparse, parse_qs

from dotenv import load_dotenv
load_dotenv()

def check_ssl_connection():
    # Récupère DATABASE_URL depuis l'environnement
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        print("❌ DATABASE_URL non trouvée dans les variables d'environnement.")
        return

    parsed_url = urlparse(database_url)
    params = parse_qs(parsed_url.query)

    # Vérifie si sslmode=require est présent
    ssl_mode = params.get("sslmode", [""])[0]
    if ssl_mode != "require":
        print("❌ ATTENTION : sslmode=require n'est PAS présent dans la DATABASE_URL !")
        print(f"URL actuelle : {database_url}")
        return

    try:
        # Connexion SSL forcée
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        print(f"✅ Connexion SSL établie avec succès !\nPostgreSQL version: {result[0]}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Échec de la connexion SSL : {e}")

if __name__ == "__main__":
    check_ssl_connection()

