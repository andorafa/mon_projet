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

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True
    }

    @app.route('/')
    def root_redirect():
        return redirect('/swagger')

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
    from app.resources.crm_api import ns as crm_ns
    from app.resources.erp_api import ns as erp_ns

    api.add_namespace(webshop_ns, path="/api/webshop")
    api.add_namespace(revendeurs_ns, path="/api/revendeurs")
    api.add_namespace(user_ns, path="/api/users")
    api.add_namespace(product_ns, path="/api/products")
    api.add_namespace(admin_ns, path="/api/admin")
    api.add_namespace(crm_ns, path="/api/crm")
    api.add_namespace(erp_ns, path="/api/erp")

    ns_health = api.namespace('health', description='Health check API')

    @ns_health.route('')
    class HealthCheck(Resource):
        def get(self):
            """Health check endpoint."""
            return {"status": "API OK"}, 200

    api.add_namespace(ns_health, path='/health')

    return app
