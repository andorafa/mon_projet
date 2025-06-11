from flask import Flask  # ✅ Corrigé
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # ✅ Connexion vérifiée avant chaque requête
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True
    }

    db.init_app(app)
    migrate.init_app(app, db)

    from flask_restful import Api
    api = Api(app)

    # Importer les ressources
    from app.resources.webshop import WebshopAPI
    from app.resources.revendeurs import RevendeursAPI
    from app.resources.user import UserAPI
    from app.resources.authenticate import AuthenticateAPI
    from app.resources.logout import LogoutAPI
    from app.resources.product_detail import ProductDetailAPI
    from app.resources.init_db import InitDBAPI

    api.add_resource(WebshopAPI, '/api/webshop/products')
    api.add_resource(RevendeursAPI, '/api/revendeurs/products')
    api.add_resource(UserAPI, '/api/users')
    api.add_resource(AuthenticateAPI, '/api/revendeurs/authenticate')
    api.add_resource(LogoutAPI, '/api/logout')
    api.add_resource(ProductDetailAPI, '/api/products/<int:product_id>')
    api.add_resource(InitDBAPI, '/api/admin/init-db')

    # ✅ Ajout de la route /
    @app.route("/")
    def health_check():
        return {"status": "API is running"}, 200

    return app
