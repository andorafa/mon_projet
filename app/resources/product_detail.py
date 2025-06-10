# app/resources/product_detail.py
from flask_restful import Resource
from app.models import Product
from app import db

class ProductDetailAPI(Resource):
    def get(self, product_id):
        product = db.session.get(Product, product_id)
        if not product:
            return {"message": "Produit introuvable."}, 404

        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "model_url": product.model_url
        }, 200
