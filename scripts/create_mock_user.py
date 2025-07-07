
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Vérifie si la clé existe déjà
    existing = User.query.filter_by(api_key="mock-api-key").first()
    if existing:
        print("✅ Clé mock-api-key déjà existante, pas besoin de recréer.")
    else:
        user = User(email="mock@test.com", api_key="mock-api-key", first_name="Mock", last_name="User")
        db.session.add(user)
        db.session.commit()
        print("✅ User avec mock-api-key créé avec succès.")
