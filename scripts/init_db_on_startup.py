# scripts/init_db_on_startup.py
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Product
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()

app = create_app()

def table_exists(table_name: str) -> bool:
    """Vérifie si une table existe dans la base."""
    inspector = db.inspect(db.engine)
    return table_name in inspector.get_table_names()

def product_table_is_empty() -> bool:
    """Vérifie si la table Product est vide."""
    return Product.query.count() == 0

def insert_default_products():
    """Insère des produits par défaut si la table est vide."""
    produits = [
        Product(
            name="Machine à Café",
            description="Machine professionnelle pour cafés gourmets",
            price=250.0,
            model_url="https://drive.google.com/uc?export=download&id=1Oq_vVepdhZqbhX2Gm7nVcQqttLrlwZWQ"
        ),
        Product(
            name="Cappuccino",
            description="Délicieux cappuccino crémeux avec une touche de cacao",
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
    db.session.add_all(produits)
    db.session.commit()
    print("✅ Produits par défaut insérés.")

def init_db_on_startup():
    """Point d'entrée : crée les tables si besoin et insère les données."""
    with app.app_context():
        try:
            print("🔎 Vérification de la base de données...")

            if not table_exists("users") or not table_exists("product"):
                print("📦 Création des tables nécessaires...")
                db.create_all()
                print("✅ Tables créées avec succès.")
            else:
                print("✔️ Tables déjà existantes.")

            if product_table_is_empty():
                print("📭 Table 'product' vide ➜ insertion des données...")
                insert_default_products()
            else:
                print("✔️ Table 'product' déjà peuplée.")

        except OperationalError as e:
            print(f"❌ Erreur de connexion à la base : {e}")
        except Exception as e:
            print(f"❌ Erreur pendant l'initialisation : {e}")

if __name__ == "__main__":
    init_db_on_startup()
