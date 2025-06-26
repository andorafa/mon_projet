from flask_restx import Namespace, Resource, fields
from flask import request, abort
from app.mock_data.mock_erp_data import get_mock_products
from app.models import Product, User
from app import db

ns = Namespace("revendeurs", description="API Revendeurs")

product_model = ns.model("Product", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "model_url": fields.String
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
        return Product.query.all()

@ns.route("/authenticate")
class AuthenticateAPI(Resource):
    @ns.doc(security="API Key")
    def post(self):
        api_key = request.headers.get("x-api-key")
        if not api_key:
            abort(400, description="Clé API manquante")
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return {"message": "Authentification réussie", "user_email": user.email}, 200
        abort(401, description="Clé invalide")

@ns.route("/logout")
class LogoutAPI(Resource):
    @ns.doc(security="API Key")
    def post(self):
        api_key = request.headers.get("x-api-key")
        if not api_key:
            abort(400, description="Clé manquante")
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            abort(401, description="Clé invalide")
        user.api_key = None
        db.session.commit()
        return {"message": "Déconnexion réussie"}, 200
