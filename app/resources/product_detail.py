from flask_restx import Namespace, Resource, fields
from app.models import Product
from app import db

ns = Namespace("products", description="Détail produit")

product_model = ns.model("Product", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "model_url": fields.String
})

@ns.route("/<int:product_id>")
class ProductDetailAPI(Resource):
    @ns.marshal_with(product_model)
    @ns.response(404, "Produit introuvable")
    def get(self, product_id):
        product = db.session.get(Product, product_id)
        if not product:
            return {"message": "Produit introuvable"}, 404
        return product
