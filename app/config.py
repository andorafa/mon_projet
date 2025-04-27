import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///mon_projet.db')

    # Ajout automatique de sslmode=require si PostgreSQL détecté
    if SQLALCHEMY_DATABASE_URI.startswith("postgresql://") and "sslmode" not in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI += "?sslmode=require"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_WEBSHOP_KEY = os.environ.get('API_WEBSHOP_KEY', 'webshop_default_key')






