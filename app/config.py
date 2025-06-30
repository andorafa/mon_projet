import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///mon_projet.db')

    if SQLALCHEMY_DATABASE_URI.startswith("postgresql://") and "sslmode" not in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI += "?sslmode=require"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_WEBSHOP_KEY = os.environ.get('API_WEBSHOP_KEY', 'webshop_default_key')

    # ➕ URL du mock centralisée ici
    MOCK_API_URL = os.environ.get(
        'MOCK_API_URL',
        'https://615f5fb4f7254d0017068109.mockapi.io/api/v1'
    )


DEBUG_CI_TEST = True
