# app/resources/revendeurs.py
from flask_restful import Resource
from flask import request, abort
from app.models import Product, User



class RevendeursAPI(Resource):
    def get(self):
        # Récupérer la clé d'API envoyée dans le header
        api_key = request.headers.get("x-api-key")
        if not api_key:
            abort(401, description="Clé d'API manquante.")

        # Vérifier que la clé correspond à un utilisateur existant dans la base de données
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            abort(401, description="Clé d'API invalide.")
        

        # Récupérer les produits (filtrage ou autres règles spécifiques peuvent être appliqués)
        products = Product.query.all()
        produits = [
            {"id": p.id, "name": p.name, "description": p.description, "price": p.price, "model_url": p.model_url}
            for p in products
        ]
        return {"products": produits}, 200
