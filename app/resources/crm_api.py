from flask_restx import Namespace, Resource, fields
from app.mock_data import mock_crm_data

ns = Namespace("crm", description="API CRM - Clients, Commandes")

client_model = ns.model("Client", {
    "id": fields.String,
    "name": fields.String,
})

order_model = ns.model("Order", {
    "id": fields.String,
    "customerId": fields.String,
    "date": fields.String,
})

product_model = ns.model("Product", {
    "id": fields.String,
    "name": fields.String,
    "price": fields.Float,
})


@ns.route("/customers")
class CustomersAPI(Resource):
    @ns.marshal_list_with(client_model)
    def get(self):
        return mock_crm_data.customers


@ns.route("/customers/<string:customer_id>/orders")
class OrdersAPI(Resource):
    @ns.marshal_list_with(order_model)
    def get(self, customer_id):
        return mock_crm_data.orders_by_customer.get(customer_id, [])


@ns.route("/customers/<string:customer_id>/orders/<string:order_id>/products")
class ProductsAPI(Resource):
    @ns.marshal_list_with(product_model)
    def get(self, customer_id, order_id):
        return mock_crm_data.products_by_order.get(order_id, [])
