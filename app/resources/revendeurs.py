from flask_restx import Namespace, Resource, fields
from flask import request, abort
from app.models import Product, User
from app import db
import requests
import os
from app.config import Config
from app.resources.common_utils import parse_mock_product, validate_api_key

ns = Namespace("revendeurs", description="API Revendeurs")

# 🔁 Constantes
ERP_API_ERROR = "Données ERP indisponibles : API mock hors ligne."
NO_PRODUCTS_LOCAL = "Aucun produit disponible dans la base locale."
API_KEY_MISSING = "Clé API manquante."
API_KEY_INVALID = "Clé API invalide."

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
            abort(401, description=API_KEY_MISSING)
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            abort(401, description=API_KEY_INVALID)

        if os.getenv("USE_MOCK_PRODUCTS", "false").lower() == "true":
            print("🟡 USE_MOCK_PRODUCTS=true ➔ récupération depuis le mock ERP.")
            try:
                url = f"{Config.MOCK_API_URL}/products"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                return [parse_mock_product(p) for p in response.json()]
            except requests.RequestException as e:
                print(f"⚠️ API mock indisponible : {e}")
                abort(503, ERP_API_ERROR)
        else:
            print("🟢 USE_MOCK_PRODUCTS=false ➔ récupération depuis la base locale.")
            products = Product.query.all()
            if products:
                return products
            else:
                abort(503, NO_PRODUCTS_LOCAL)


@ns.route("/products/<int:product_id>")
class RevendeurProductDetailAPI(Resource):
    @ns.doc(security="API Key")
    @ns.marshal_with(product_model)
    @ns.response(404, "Produit introuvable")
    def get(self, product_id):
        api_key = request.headers.get("x-api-key")
        if not api_key:
            abort(401, description=API_KEY_MISSING)
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            abort(401, description=API_KEY_INVALID)

        if os.getenv("USE_MOCK_PRODUCTS", "false").lower() == "true":
            print("🟡 USE_MOCK_PRODUCTS=true ➔ récupération détail depuis le mock ERP.")
            try:
                url = f"{Config.MOCK_API_URL}/products/{product_id}"
                response = requests.get(url, timeout=5)
                if response.status_code == 404:
                    abort(404, f"Produit {product_id} non trouvé sur l'API mock")
                response.raise_for_status()
                return parse_mock_product(response.json())
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
            abort(400, description=API_KEY_MISSING)
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            abort(401, description=API_KEY_INVALID)
        return {"message": "Authentification réussie"}, 200


@ns.route("/logout")
class RevendeurLogout(Resource):
    @ns.doc(security="API Key")
    def post(self):
        api_key = request.headers.get("x-api-key")
        if not api_key:
            abort(400, description=API_KEY_MISSING)
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            abort(401, description=API_KEY_INVALID)
        db.session.delete(user)
        db.session.commit()
        return {"message": "Déconnexion réussie"}, 200
