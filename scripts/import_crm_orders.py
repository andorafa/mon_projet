# scripts/import_crm_orders.py

from datetime import date as dt_date, datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from sqlalchemy import text
from app import create_app, db
from app.models import Customer, Order, OrderProduct
from app.config import Config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
app = create_app()

def import_crm_orders():
    with app.app_context():
        print("🚀 Démarrage de l'import des clients et commandes CRM...")

        # Nettoyage des tables
        db.session.execute(text("DELETE FROM order_product;"))
        db.session.execute(text("DELETE FROM \"order\";"))
        db.session.execute(text("DELETE FROM customer;"))
        db.session.commit()
        print("✅ Tables nettoyées.")

        # Récupérer les clients depuis le mock
        print("🔎 Téléchargement des clients depuis l'API mock CRM...")
        try:
            response = requests.get(f"{Config.MOCK_API_URL}/customers", timeout=10)
            response.raise_for_status()
            customers_mock = response.json()
        except Exception as e:
            print(f"❌ Échec récupération clients : {e}")
            return

        clients = []
        for c in customers_mock:
            try:
                cust = Customer(
                    id=int(c["id"]),
                    name=c.get("name", ""),
                    first_name=c.get("firstName", ""),
                    last_name=c.get("lastName", ""),
                    city=c.get("address", {}).get("city", ""),
                    postal_code=c.get("address", {}).get("postalCode", "")
                )
                db.session.add(cust)
                clients.append(cust)
            except Exception as e:
                print(f"⚠️ Client ignoré : {e}")

        db.session.commit()
        print(f"✅ {len(clients)} clients insérés.")

        # Pour chaque client, récupérer les commandes
        total_orders = 0
        total_order_products = 0
        for cust in clients:
            print(f"📦 Téléchargement des commandes pour le client ID={cust.id}...")
            try:
                response = requests.get(f"{Config.MOCK_API_URL}/customers/{cust.id}", timeout=10)
                response.raise_for_status()
                customer_data = response.json()
            except Exception as e:
                print(f"❌ Impossible de récupérer le client {cust.id} : {e}")
                continue

            orders = customer_data.get("orders", [])
            for o in orders:
                try:
                    order = Order(
                        id=o["id"],
                        customer_id=cust.id,
                        date=datetime.now(tz=datetime.UTC),
                        status="imported",
                        total_amount=0.0  # peut être recalculé si besoin
                    )
                    db.session.add(order)
                    total_orders += 1

                    # Produits de la commande
                    products = o.get("products", [])
                    for p in products:
                        try:
                            op = OrderProduct(
                                order_id=o["id"],
                                product_name=p.get("name", ""),
                                quantity=int(p.get("quantity", 1)),
                                price=float(str(p.get("price", "0")).replace(',', '.'))
                            )
                            db.session.add(op)
                            total_order_products += 1
                        except Exception as e:
                            print(f"⚠️ Produit ignoré pour commande {o['id']}: {e}")
                except Exception as e:
                    print(f"⚠️ Commande ignorée : {e}")

        db.session.commit()
        print(f"🎉 Import terminé : {total_orders} commandes, {total_order_products} produits insérés.")

if __name__ == "__main__":
    import_crm_orders()
