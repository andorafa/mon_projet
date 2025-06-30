# scripts/full_reset.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from sqlalchemy import text
from app import create_app, db
from app.models import Product, Customer
from app.config import Config

app = create_app()

def reset_and_populate_erp():
    print("\n📦 [ERP] Réinitialisation de la table Product...")
    inspector = db.inspect(db.engine)
    if 'product' not in inspector.get_table_names():
        print("❌ Table 'product' non trouvée. Vérifiez vos migrations ou vos modèles.")
        return

    db.session.execute(text("DELETE FROM product;"))
    db.session.commit()

    print("🔎 Téléchargement des produits depuis l'API mock ERP...")
    try:
        response = requests.get(f"{Config.MOCK_API_URL}/products", timeout=10)
        response.raise_for_status()
        products_mock = response.json()
    except Exception as e:
        print(f"❌ Échec récupération API mock ERP : {e}")
        return

    produits = []
    for p in products_mock:
        try:
            price_str = str(p.get("details", {}).get("price", "0")).replace(',', '.')
            produits.append(Product(
                name=p["name"],
                description=p.get("details", {}).get("description", ""),
                price=float(price_str),
                model_url=""
            ))
        except Exception as e:
            print(f"⚠️ Produit ignoré : {e}")

    if produits:
        try:
            db.session.add_all(produits)
            db.session.commit()
            print(f"✅ {len(produits)} produits insérés avec succès.")
        except Exception as e:
            print(f"❌ Échec insertion produits : {e}")
    else:
        print("⚠️ Aucun produit inséré.")

def reset_and_populate_crm():
    print("\n📦 [CRM] Réinitialisation des tables Customer + Orders...")

    inspector = db.inspect(db.engine)
    if 'customer' not in inspector.get_table_names():
        print("❌ Table 'customer' non trouvée. Vérifiez vos migrations ou vos modèles.")
        return

    # ⚠️ Supprimer dans l'ordre pour éviter les violations de contraintes
    db.session.execute(text("DELETE FROM order_product;"))
    db.session.execute(text("DELETE FROM \"order\";"))  # "order" entre guillemets car mot réservé SQL
    db.session.execute(text("DELETE FROM customer;"))
    db.session.commit()

    print("🔎 Téléchargement des clients depuis l'API mock CRM...")
    try:
        response = requests.get(f"{Config.MOCK_API_URL}/customers", timeout=10)
        response.raise_for_status()
        customers_mock = response.json()
    except Exception as e:
        print(f"❌ Échec récupération API mock CRM : {e}")
        return

    clients = []
    for c in customers_mock:
        try:
            clients.append(Customer(
                id=int(c["id"]),
                name=c.get("name", ""),
                first_name=c.get("firstName", ""),
                last_name=c.get("lastName", ""),
                city=c.get("address", {}).get("city", ""),
                postal_code=c.get("address", {}).get("postalCode", "")
            ))
        except Exception as e:
            print(f"⚠️ Client ignoré : {e}")

    if clients:
        try:
            db.session.add_all(clients)
            db.session.commit()
            print(f"✅ {len(clients)} clients insérés avec succès.")
        except Exception as e:
            print(f"❌ Échec insertion clients : {e}")
    else:
        print("⚠️ Aucun client inséré.")

def reset_and_populate_all():
    with app.app_context():
        print("\n🚀 Initialisation complète de la base de données...")
        db.create_all()
        reset_and_populate_erp()
        reset_and_populate_crm()
        print("\n🎉 Base de données initialisée avec succès.")

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    reset_and_populate_all()
