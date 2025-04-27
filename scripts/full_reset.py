# scripts/full_reset.py
import sys
import os
from sqlalchemy import text
from app import create_app, db
from app.models import Product

app = create_app()

def reset_and_populate():
    with app.app_context():
        # 1. Créer les tables d'abord
        print("📦 Création des tables...")
        db.create_all()

        # 2. Puis seulement reset
        database_url = app.config['SQLALCHEMY_DATABASE_URI']

        if database_url.startswith("sqlite"):
            print("⚡ Base SQLite détectée ➔ DELETE FROM...")
            try:
                db.session.execute(text("DELETE FROM products;"))
                db.session.commit()
            except Exception as e:
                print(f"❌ Erreur DELETE : {e}")
        else:
            print("⚡ Base PostgreSQL détectée ➔ TRUNCATE TABLE...")
            db.session.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE;"))
            db.session.commit()

        print("✅ Table products vidée.")

        # 3. Puis seulement insérer
        produits = [
            Product(name="Machine à Café", description="Machine professionnelle pour préparation de cafés gourmets", price=250.0),
            Product(name="Café Latté", description="Un délicieux café au lait", price=3.5),
            Product(name="Espresso", description="Un café noir intense", price=2.0),
            Product(name="Cappuccino", description="Un cappuccino mousseux italien", price=4.0),
            Product(name="Thé Vert", description="Un thé vert bio rafraîchissant", price=2.5),
            Product(name="Chocolat Chaud", description="Chocolat chaud réconfortant", price=3.0)
        ]

        db.session.add_all(produits)
        db.session.commit()
        print("✅ Produits de test insérés avec succès.")

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    reset_and_populate()
