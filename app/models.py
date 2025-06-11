# app/models.py
from app import db
from sqlalchemy import Column, Integer, String, DateTime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    price = db.Column(db.Float, nullable=False)
    model_url = db.Column(db.String(512))

    def __repr__(self):
        return f"<Product {self.name}>"

class User(db.Model):
    __tablename__ = 'users'  
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    api_key = db.Column(db.String(64), unique=True, nullable=True)

    def __repr__(self):
        return f"<User {self.email}>"
