from flask_restx import Namespace, Resource, fields
from flask import request, abort
from app.models import Product
from app.config import Config
from app import db
import requests

ns = Namespace("webshop", description="API Webshop")

product_model = ns.model("Product", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "model_url": fields.String,
    "created_at": fields.String,     # ➕ ajouté
    "stock": fields.Integer,         # ➕ ajouté
})

@ns.route("/products")
class WebshopAPI(Resource):
    @ns.doc(security="API Key")
    @ns.marshal_with(product_model, as_list=True)
    def get(self):
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key != Config.API_WEBSHOP_KEY:
            abort(401, description="Clé API invalide ou manquante")

        try:
            url = f"{Config.MOCK_API_URL}/products"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            products_mock = response.json()
            cleaned = []
            for p in products_mock:
                price_str = str(p.get("details", {}).get("price", "0")).replace(',', '.')
                cleaned.append({
                    "id": int(p["id"]),
                    "name": p["name"],
                    "description": p.get("details", {}).get("description", ""),
                    "price": float(price_str),
                    "model_url": "",
                    "created_at": p.get("createdAt", ""),  # ➕ récupéré
                    "stock": int(p.get("stock", 0)) if isinstance(p.get("stock", 0), int) else 0,  # ➕ récupéré
                })
            return cleaned

        except requests.RequestException as e:
            print(f"⚠️ API mock indisponible : {e}, fallback sur la BDD...")
            products = Product.query.all()
            if products:
                return products
            else:
                abort(503, "Aucune donnée disponible : API mock hors ligne et base locale vide.")

@ns.route("/products/<int:product_id>")
class WebshopProductDetail(Resource):
    @ns.doc(security="API Key")
    @ns.marshal_with(product_model)
    def get(self, product_id):
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key != Config.API_WEBSHOP_KEY:
            abort(401, description="Clé API invalide ou manquante")

        # 🔎 Essayer d'abord depuis le mock
        try:
            url = f"{Config.MOCK_API_URL}/products/{product_id}"
            response = requests.get(url, timeout=5)
            if response.status_code == 404:
                abort(404, f"Produit {product_id} introuvable sur l'API mock")
            response.raise_for_status()
            p = response.json()
            price_str = str(p.get("details", {}).get("price", "0")).replace(',', '.')
            return {
                "id": int(p["id"]),
                "name": p["name"],
                "description": p.get("details", {}).get("description", ""),
                "price": float(price_str),
                "model_url": "",  # Le mock n'a pas d'URL modèle
                "created_at": p.get("createdAt", ""),
                "stock": int(p.get("stock", 0)) if isinstance(p.get("stock", 0), int) else 0,
            }
        except requests.RequestException as e:
            print(f"⚠️ API mock indisponible : {e}, fallback sur la BDD...")

            # ➔ fallback sur la base locale
            product = db.session.get(Product, product_id)
            if product:
                return product
            else:
                abort(404, f"Produit {product_id} introuvable dans la base locale.")

