import os
from dotenv import load_dotenv
from flask import Flask

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

app = Flask(__name__)
api = Api(app)


load_dotenv()  # Charge les variables d'environnement depuis le fichier .env

# Configuration du secret pour signer les JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Utilise la variable d'environnement

jwt = JWTManager(app)

# Mock des données de l'ERP et du CRM
products = [
    {'id': 1, 'name': 'Café Robusta', 'description': 'Café fort', 'price': 10},
    {'id': 2, 'name': 'Café Arabica', 'description': 'Café doux', 'price': 12}
]

customers = [
    {'id': 1, 'name': 'Client A'},
    {'id': 2, 'name': 'Client B'}
]

# API Webshop (produits)
class ProductList(Resource):
    def get(self):
        return jsonify(products)

class ProductDetail(Resource):
    def get(self, product_id):
        product = next((prod for prod in products if prod['id'] == product_id), None)
        if product:
            return jsonify(product)
        return {'message': 'Produit non trouvé'}, 404

# API Revendeurs (clients)
class CustomerList(Resource):
    def get(self):
        return jsonify(customers)

# Ajouter les routes
api.add_resource(ProductList, '/api/v1/products')
api.add_resource(ProductDetail, '/api/v1/products/<int:product_id>')
api.add_resource(CustomerList, '/api/v1/customers')

if __name__ == '__main__':
    app.run(debug=True)
