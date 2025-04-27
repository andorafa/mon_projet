# app/__init__.py
from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Initialisation de la base de données et des migrations
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Création de l'API REST avec Flask-RESTful
    from flask_restful import Api
    api = Api(app)


    
    # Importer et enregistrer les ressources (endpoints)
    from app.resources.webshop import WebshopAPI
    from app.resources.revendeurs import RevendeursAPI
    
    api.add_resource(WebshopAPI, '/api/webshop/products')
    api.add_resource(RevendeursAPI, '/api/revendeurs/products')
    
    
    # Ajout du nouvel endpoint pour la gestion des utilisateurs
    from app.resources.user import UserAPI
    from app.resources.authenticate import AuthenticateAPI
    api.add_resource(UserAPI, '/api/users')
    api.add_resource(AuthenticateAPI, '/api/revendeurs/authenticate')

    #deconnexion
    from app.resources.logout import LogoutAPI
    api.add_resource(LogoutAPI, '/api/logout')  # endpoint de déconnexion


    return app
