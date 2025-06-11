from flask_restful import Resource
from flask import request, abort
from app.models import Product, User
from app.config import Config


class WebshopAPI(Resource):
    def get(self):
        api_key = request.headers.get("x-api-key")

        # ✅ Vérifie l'existence d’un utilisateur ou fallback via config
        user = User.query.filter_by(api_key=api_key).first()
        if not user and api_key != Config.API_WEBSHOP_KEY:
            abort(401, description="Clé API invalide")

        # ✅ Récupère les produits depuis la BDD
        products = Product.query.all()
        produits = [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": p.price
            } for p in products
        ]

        return {"products": produits}, 200
