from flask_restful import Resource, abort
from flask import request
from app.models import User
from app import db

class LogoutAPI(Resource):
    def post(self):
        # 1) Récupère la clé API dans l'en‑tête
        api_key = request.headers.get("x-api-key")
        if not api_key:
            abort(400, description="Clé d'API manquante")

        # 2) Cherche l'utilisateur correspondant
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            abort(401, description="Clé d'API invalide")

        # 3) Invalide la clé en base
        user.api_key = None
        db.session.commit()

        return {"message": "Déconnexion réussie"}, 200