# app/config.py
import os

class Config:
    # Base de données : Render te fournit DATABASE_URL automatiquement
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///mon_projet.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clé secrète Flask pour la sécurité
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')

    # Clé API pour sécuriser l'accès au Webshop
    API_WEBSHOP_KEY = os.environ.get('API_WEBSHOP_KEY', 'webshop_default_key')





