from flask_restx import Namespace, Resource, fields
from flask import request, abort
from app.mock_data.mock_erp_data import get_mock_products
from app.models import Product, User
from app.config import Config

ns = Namespace("webshop", description="API Webshop")

product_model = ns.model("Product", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "model_url": fields.String
})

@ns.route("/products")
class WebshopAPI(Resource):
    @ns.doc(security="API Key")
    @ns.marshal_with(product_model, as_list=True)
    @ns.response(401, "Clé API invalide")
    def get(self):
        api_key = request.headers.get("x-api-key")
        user = User.query.filter_by(api_key=api_key).first()
        if not api_key or (not user and api_key != Config.API_WEBSHOP_KEY):
            abort(401, description="Clé API invalide ou manquante")
        return get_mock_products()
