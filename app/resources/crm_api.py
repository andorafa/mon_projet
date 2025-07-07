import requests
from flask_restx import Namespace, Resource, fields
from app.config import Config

ns = Namespace("crm", description="API CRM - Clients et Commandes")

# 🔁 Constantes
CRM_API_ERROR_MESSAGE = "Données CRM indisponibles : API mock hors ligne."

customer_model = ns.model("Customer", {
    "id": fields.String,
    "name": fields.String,
    "firstName": fields.String,
    "lastName": fields.String,
    "city": fields.String(attribute="address.city"),
    "postalCode": fields.String(attribute="address.postalCode"),
})

@ns.route("/customers")
class CustomersAPI(Resource):
    @ns.marshal_list_with(customer_model)
    def get(self):
        try:
            url = f"{Config.MOCK_API_URL}/customers"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"⚠️ API mock CRM indisponible : {e}")
            ns.abort(503, CRM_API_ERROR_MESSAGE)

@ns.route("/customers/<string:customer_id>/orders")
class CustomerOrdersAPI(Resource):
    def get(self, customer_id):
        try:
            url = f"{Config.MOCK_API_URL}/customers/{customer_id}"
            response = requests.get(url, timeout=5)
            if response.status_code == 404:
                ns.abort(404, f"Client {customer_id} introuvable sur l'API mock")
            response.raise_for_status()
            customer = response.json()
            return customer.get("orders", [])
        except requests.RequestException as e:
            print(f"⚠️ API mock CRM indisponible : {e}")
            ns.abort(503, CRM_API_ERROR_MESSAGE)

@ns.route("/customers/<string:customer_id>/orders/<string:order_id>/products")
class OrderProductsAPI(Resource):
    def get(self, customer_id, order_id):
        try:
            url = f"{Config.MOCK_API_URL}/customers/{customer_id}"
            response = requests.get(url, timeout=5)
            if response.status_code == 404:
                ns.abort(404, f"Client {customer_id} introuvable sur l'API mock")
            response.raise_for_status()
            customer = response.json()
            orders = customer.get("orders", [])
            for order in orders:
                if order.get("id") == order_id:
                    return order.get("products", [])
            ns.abort(404, f"Commande {order_id} non trouvée pour le client {customer_id}")
        except requests.RequestException as e:
            print(f"⚠️ API mock CRM indisponible : {e}")
            ns.abort(503, CRM_API_ERROR_MESSAGE)
