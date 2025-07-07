import pytest
from app import db
from app.models import Customer, Product, Order, OrderProduct

def test_order_product_relationship(client):
    with client.application.app_context():
        # 1️⃣ Créer un client
        customer = Customer(id=1, name="Test Client", first_name="Jean", last_name="Durand")
        db.session.add(customer)
        db.session.commit()

        # 2️⃣ Créer un produit
        product = Product(name="Machine Test", description="Test produit", price=42.0, stock=5)
        db.session.add(product)
        db.session.commit()

        # 3️⃣ Créer une commande
        order = Order(id="CMD-001", customer_id=customer.id, status="pending")
        db.session.add(order)
        db.session.commit()

        # 4️⃣ Créer un OrderProduct lié
        op = OrderProduct(
            order_id=order.id,
            product_id=product.id,
            product_name=product.name,
            quantity=2,
            price=product.price
        )
        db.session.add(op)
        db.session.commit()

        # 5️⃣ Vérifier la relation produit
        fetched_op = OrderProduct.query.get(op.id)
        assert fetched_op.product.name == "Machine Test"
        assert fetched_op.order.id == "CMD-001"
