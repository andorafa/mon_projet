from flask_restx import Namespace, Resource, fields
from flask import request, abort
from app.models import Product
from app.config import Config
from app import db
import requests
from app.resources.common_utils import parse_mock_product, validate_api_key

ns = Namespace("webshop", description="API Webshop")

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
class WebshopAPI(Resource):
    @ns.doc(security="API Key")
    @ns.marshal_with(product_model, as_list=True)
    def get(self):
        api_key = request.headers.get("x-api-key")
        validate_api_key(api_key, Config.API_WEBSHOP_KEY)

        try:
            url = f"{Config.MOCK_API_URL}/products"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            products_mock = response.json()
            return [parse_mock_product(p) for p in products_mock]

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
        validate_api_key(api_key, Config.API_WEBSHOP_KEY)

        try:
            url = f"{Config.MOCK_API_URL}/products/{product_id}"
            response = requests.get(url, timeout=5)
            if response.status_code == 404:
                abort(404, f"Produit {product_id} introuvable sur l'API mock")
            response.raise_for_status()
            return parse_mock_product(response.json())

        except requests.RequestException as e:
            print(f"⚠️ API mock indisponible : {e}, fallback sur la BDD...")
            product = db.session.get(Product, product_id)
            if product:
                return product
            else:
                abort(404, f"Produit {product_id} introuvable dans la base locale.")
