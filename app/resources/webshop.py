# app/resources/webshop.py
from flask_restful import Resource
from flask import Config, request, abort
from app.models import Product
from app.config import Config

class WebshopAPI(Resource):
    def get(self):
        # Vérifier la clé API dans les headers
        api_key = request.headers.get("x-api-key")
        if api_key != Config.API_WEBSHOP_KEY:
            abort(401, description="Accès non autorisé")
        
        # Récupérer les produits depuis la base de données
        products = Product.query.all()
        produits = [
            {"id": p.id, "name": p.name, "description": p.description, "price": p.price}
            for p in products
        ]
        return {"products": produits}, 200
