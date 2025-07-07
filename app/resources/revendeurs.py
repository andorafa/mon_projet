from flask_restx import Namespace, Resource, fields
from flask import request, abort
from app.models import Product, User
from app import db
import requests
import os  # ← Ajouté
from app.config import Config

ns = Namespace("revendeurs", description="API Revendeurs")

product_model = ns.model("Product", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "model_url": fields.String,
    "created_at": fields.String,
    "stock": fields.Integer,
})

@ns.route("/products")
class RevendeursAPI(Resource):
    @ns.doc(security="API Key")
    @ns.marshal_with(product_model, as_list=True)
    def get(self):
        api_key = request.headers.get("x-api-key")
        if not api_key:
            abort(401, description="Clé API manquante.")
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            abort(401, description="Clé API invalide.")

        if os.getenv("USE_MOCK_PRODUCTS", "false").lower() == "true":
            print("🟡 USE_MOCK_PRODUCTS=true ➔ récupération depuis le mock ERP.")
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
                        "created_at": p.get("createdAt", ""),
                        "stock": int(p.get("stock", 0)) if isinstance(p.get("stock", 0), int) else 0,
                    })
                return cleaned
            except requests.RequestException as e:
                print(f"⚠️ API mock indisponible : {e}")
                abort(503, "Données ERP indisponibles : API mock hors ligne.")
        else:
            print("🟢 USE_MOCK_PRODUCTS=false ➔ récupération depuis la base locale.")
            products = Product.query.all()
            if products:
                return products
            else:
                abort(503, "Aucun produit disponible dans la base locale.")

@ns.route("/products/<int:product_id>")
class RevendeurProductDetailAPI(Resource):
    @ns.doc(security="API Key")
    @ns.marshal_with(product_model)
    @ns.response(404, "Produit introuvable")
    def get(self, product_id):
        api_key = request.headers.get("x-api-key")
        if not api_key:
            abort(401, description="Clé API manquante.")
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            abort(401, description="Clé API invalide.")

        if os.getenv("USE_MOCK_PRODUCTS", "false").lower() == "true":
            print("🟡 USE_MOCK_PRODUCTS=true ➔ récupération détail depuis le mock ERP.")
            try:
                url = f"{Config.MOCK_API_URL}/products/{product_id}"
                response = requests.get(url, timeout=5)
                if response.status_code == 404:
                    abort(404, f"Produit {product_id} non trouvé sur l'API mock")
                response.raise_for_status()
                p = response.json()
                price_str = str(p.get("details", {}).get("price", "0")).replace(',', '.')
                return {
                    "id": int(p["id"]),
                    "name": p["name"],
                    "description": p.get("details", {}).get("description", ""),
                    "price": float(price_str),
                    "model_url": "",
                    "created_at": p.get("createdAt", ""),
                    "stock": int(p.get("stock", 0)) if isinstance(p.get("stock", 0), int) else 0,
                }
            except requests.RequestException as e:
                print(f"⚠️ API mock indisponible : {e}")
                abort(503, f"Service indisponible pour récupérer le produit {product_id}.")
        else:
            print("🟢 USE_MOCK_PRODUCTS=false ➔ récupération détail depuis la base locale.")
            product = db.session.get(Product, product_id)
            if product:
                return product
            else:
                abort(404, f"Produit {product_id} introuvable dans la base locale.")

@ns.route("/authenticate")
class RevendeurAuthenticate(Resource):
    @ns.doc(security="API Key")
    def post(self):
        api_key = request.headers.get("x-api-key")
        if not api_key:
            abort(400, description="Clé API manquante.")
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            abort(401, description="Clé API invalide.")
        return {"message": "Authentification réussie"}, 200

@ns.route("/logout")
class RevendeurLogout(Resource):
    @ns.doc(security="API Key")
    def post(self):
        api_key = request.headers.get("x-api-key")
        if not api_key:
            abort(400, description="Clé API manquante.")
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            abort(401, description="Clé API invalide.")
        db.session.delete(user)
        db.session.commit()
        return {"message": "Déconnexion réussie"}, 200
