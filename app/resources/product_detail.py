from flask_restx import Namespace, Resource, fields
from app.models import Product
from app import db
import requests
from app.config import Config

ns = Namespace("products", description="Détail produit")

product_model = ns.model("Product", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "model_url": fields.String,
})

@ns.route("/<int:product_id>")
class ProductDetailAPI(Resource):
    @ns.marshal_with(product_model)
    @ns.response(404, "Produit introuvable")
    def get(self, product_id):
        try:
            url = f"{Config.MOCK_API_URL}/products/{product_id}"
            response = requests.get(url, timeout=5)
            if response.status_code == 404:
                ns.abort(404, f"Produit {product_id} non trouvé sur l'API mock")
            response.raise_for_status()
            p = response.json()
            return {
                "id": int(p["id"]),
                "name": p["name"],
                "description": p.get("details", {}).get("description", ""),
                "price": float(p.get("details", {}).get("price", 0)),
                "model_url": "",
            }
        except requests.RequestException as e:
            print(f"⚠️ API mock indisponible : {e}, fallback sur la BDD...")
            product = db.session.get(Product, product_id)
            if product:
                return product
            else:
                ns.abort(404, f"Produit {product_id} introuvable dans la BDD locale.")
