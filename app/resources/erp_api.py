from flask_restx import Namespace, Resource, fields
from app.mock_data import mock_erp_data

ns = Namespace("erp", description="API ERP - Produits")

# @ns.route("/products")
# class ProductsAPI(Resource):
#     def get(self):
#         return mock_erp_data.get_mock_products()


product_model = ns.model("Product", {
    "id": fields.String,
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float,
})


@ns.route("/products")
class ProductListAPI(Resource):
    @ns.marshal_list_with(product_model)
    def get(self):
        return mock_erp_data.products


@ns.route("/products/<string:product_id>")
class ProductDetailAPI(Resource):
    @ns.marshal_with(product_model)
    def get(self, product_id):
        for product in mock_erp_data.products:
            if product["id"] == product_id:
                return product
        ns.abort(404, "Produit non trouvé")
