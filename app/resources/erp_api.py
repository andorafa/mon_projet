import requests
from flask_restx import Namespace, Resource, fields
from app.config import Config
from app.models import Product
from app import db

ns = Namespace("erp", description="API ERP - Produits")

product_model = ns.model("Product", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "color": fields.String,
    "stock": fields.Integer,
    "created_at": fields.String,  # ➕ champ ajouté
})

@ns.route("/products")
class ProductListAPI(Resource):
    @ns.marshal_list_with(product_model)
    def get(self):
        try:
            url = f"{Config.MOCK_API_URL}/products"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            products = response.json()
            cleaned = []
            for p in products:
                price_str = str(p.get("details", {}).get("price", "0")).replace(',', '.')
                cleaned.append({
                    "id": int(p["id"]),
                    "name": p["name"],
                    "description": p.get("details", {}).get("description", ""),
                    "price": float(price_str),
                    "color": p.get("details", {}).get("color", ""),
                    "stock": int(p.get("stock", 0)) if isinstance(p.get("stock", 0), int) else 0,
                    "created_at": p.get("createdAt", ""),  # ➕ récupéré
                })
            return cleaned
        except requests.RequestException as e:
            print(f"⚠️ API mock ERP indisponible : {e}, fallback sur la BDD...")
            products = Product.query.all()
            if products:
                return products
            else:
                ns.abort(503, "Aucune donnée disponible : API mock ERP hors ligne et base locale vide.")

@ns.route("/products/<int:product_id>")
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
            price_str = str(p.get("details", {}).get("price", "0")).replace(',', '.')
            return {
                "id": int(p["id"]),
                "name": p["name"],
                "description": p.get("details", {}).get("description", ""),
                "price": float(price_str),
                "color": p.get("details", {}).get("color", ""),
                "stock": int(p.get("stock", 0)) if isinstance(p.get("stock", 0), int) else 0,
                "created_at": p.get("createdAt", ""),  # ➕ récupéré
            }
        except requests.RequestException as e:
            print(f"⚠️ API mock ERP indisponible : {e}, fallback sur la BDD...")
            product = db.session.get(Product, product_id)
            if product:
                return product
            else:
                ns.abort(404, f"Produit {product_id} introuvable dans la BDD locale.")
