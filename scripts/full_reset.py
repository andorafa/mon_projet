# scripts/full_reset.py

import sys
import os
from sqlalchemy import text
from app import create_app, db
from app.models import Product

app = create_app()

def reset_and_populate():
    with app.app_context():
        print("📦 Création des tables (si inexistantes)...")
        db.create_all()

        # Vérifie si la table 'products' existe bien
        inspector = db.inspect(db.engine)
        if 'product' not in inspector.get_table_names():
            print("❌ Table 'product' non trouvée. Assure-toi que le modèle est correct.")
            return

        # Nettoyage sécurisé selon le type de base
        database_url = app.config['SQLALCHEMY_DATABASE_URI']
        try:
            if database_url.startswith("sqlite"):
                print("⚡ Base SQLite ➔ DELETE FROM...")
                db.session.execute(text("DELETE FROM product;"))
            else:
                print("⚡ Base PostgreSQL ➔ TRUNCATE TABLE...")
                db.session.execute(text("TRUNCATE TABLE product RESTART IDENTITY CASCADE;"))
            db.session.commit()
            print("✅ Table 'product' vidée.")
        except Exception as e:
            print(f"❌ Erreur pendant la suppression : {e}")
            return

        # Remplissage des produits avec model_url
        produits = [
            Product(
                name="Machine à Café",
                description="Machine professionnelle pour cafés gourmets",
                price=250.0,
                model_url="https://drive.google.com/uc?export=download&id=1Oq_vVepdhZqbhX2Gm7nVcQqttLrlwZWQ"
            ),
            Product(
                name="Cappuccino",
                description="A cup_of_cappuccino",
                price=50.0,
                model_url="https://drive.google.com/uc?export=download&id=1PsD-QhE0z1R-v4mcY8-W0CFw746oLUXl"
            ),
            Product(
                name="Thé Vert",
                description="Thé bio rafraîchissant",
                price=2.5,
                model_url=""
            ),
        ]

        try:
            db.session.add_all(produits)
            db.session.commit()
            print("✅ Produits insérés avec succès.")
        except Exception as e:
            print(f"❌ Échec insertion des produits : {e}")

if __name__ == "__main__":
    # Assure l'accès au module 'app' depuis scripts/
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    reset_and_populate()
