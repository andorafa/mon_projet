# scripts/init_db_on_startup.py

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

app = create_app()

def init_db():
    with app.app_context():
        print("🔎 Initialisation de la base de données...")

        # Crée les tables si elles n'existent pas
        db.create_all()

        print("✅ Base de données initialisée avec succès.")

if __name__ == "__main__":
    init_db()
