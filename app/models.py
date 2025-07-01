from app import db
from datetime import datetime, UTC

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    api_key = db.Column(db.String(256), nullable=False, unique=True)
    first_name = db.Column(db.String(256), nullable=True)  # Ajouté pour stocker le prénom
    last_name = db.Column(db.String(256), nullable=True)   # Ajouté pour stocker le nom de famille
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} ({self.email})>"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    model_url = db.Column(db.String(1024))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    stock = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Product {self.name}>"

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # identifiant CRM
    name = db.Column(db.String(256))
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    city = db.Column(db.String(256))
    postal_code = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    orders = db.relationship("Order", backref="customer", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Customer {self.first_name} {self.last_name}>"

class Order(db.Model):
    id = db.Column(db.String(64), primary_key=True)  # identifiant commande CRM
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(tz=datetime.UTC))
    status = db.Column(db.String(128), default="pending")
    total_amount = db.Column(db.Float, default=0.0)
    products = db.relationship("OrderProduct", backref="order", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order {self.id} of Customer {self.customer_id}>"

class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(64), db.ForeignKey("order.id"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=True)  # ✅ ajout relation
    product_name = db.Column(db.String(512), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False, default=0.0)

    product = db.relationship("Product", backref="order_products")  # ✅ accès facile au produit lié

    def __repr__(self):
        return f"<OrderProduct {self.product_name} x{self.quantity} for Order {self.order_id}>"

