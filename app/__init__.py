from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api, Resource
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    authorizations = {
        "API Key": {
            "type": "apiKey",
            "in": "header",
            "name": "x-api-key"
        }
    }

    api = Api(
        app,
        title="PayeTonKawa API",
        version="1.0",
        description="Swagger pour les APIs Webshop et Revendeurs",
        doc="/swagger",
        security="API Key",
        authorizations=authorizations
    )

    from app.resources.webshop import ns as webshop_ns
    from app.resources.revendeurs import ns as revendeurs_ns
    from app.resources.user import ns as user_ns
    from app.resources.product_detail import ns as product_ns
    from app.resources.init_db import ns as admin_ns

    api.add_namespace(webshop_ns, path="/api/webshop")
    api.add_namespace(revendeurs_ns, path="/api/revendeurs")
    api.add_namespace(user_ns, path="/api/users")
    api.add_namespace(product_ns, path="/api/products")
    api.add_namespace(admin_ns, path="/api/admin")

    ns_health = api.namespace('health', description='Health check API')

    @ns_health.route('')
    class HealthCheck(Resource):
        def get(self):
            """Health check endpoint."""
            return {"status": "API OK"}, 200

    api.add_namespace(ns_health, path='/health')

    @app.route('/home')
    def home_direct():
        return redirect('/swagger')
    

    return app
