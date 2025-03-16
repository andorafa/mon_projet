from flask_restful import Resource
from flask import request, abort
from app.models import User

class AuthenticateAPI(Resource):
    def post(self):
        # Récupère la clé d'API envoyée dans le header x-api-key
        api_key = request.headers.get("x-api-key")
        if not api_key:
            abort(400, description="La clé d'API est requise.")

        # Recherche l'utilisateur correspondant à cette clé
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return {"message": "Authentification réussie", "user_email": user.email}, 200
        else:
            abort(401, description="Clé d'API invalide.")