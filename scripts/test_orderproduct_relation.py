import sys
import os

# ➜ Permet d'importer les modules du projet depuis le dossier scripts/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Customer, Product, Order, OrderProduct

app = create_app()

with app.app_context():
    # 1️⃣ Créer un customer fictif
    customer = Customer(id=1, name="Test Customer", first_name="Test", last_name="User")
    db.session.add(customer)
    db.session.commit()
    print(f"✅ Customer créé : id={customer.id}, name={customer.name}")

    # 2️⃣ Créer un produit
    product = Product(name="Test Product Relation", description="Produit pour test relation", price=42.0, stock=5)
    db.session.add(product)
    db.session.commit()
    print(f"✅ Produit créé : id={product.id}, name={product.name}")

    # 3️⃣ Créer une commande pour ce customer
    order = Order(id="TEST-ORDER-001", customer_id=customer.id, status="pending")
    db.session.add(order)
    db.session.commit()
    print(f"✅ Commande créée : id={order.id}")

    # 4️⃣ Créer un OrderProduct lié au produit créé
    order_product = OrderProduct(
        order_id=order.id,
        product_id=product.id,
        product_name=product.name,  # snapshot du nom du produit
        quantity=2,
        price=product.price
    )
    db.session.add(order_product)
    db.session.commit()
    print(f"✅ OrderProduct créé : id={order_product.id}, lié au produit id={order_product.product_id}")

    # 5️⃣ Vérifier l'accès au produit depuis order_product
    fetched_order_product = OrderProduct.query.get(order_product.id)
    print(f"🔎 Produit lié via relation : {fetched_order_product.product}")
