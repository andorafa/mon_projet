from flask_restful import Resource
from flask import request, abort
from app.models import User

class AuthenticateAPI(Resource):
    def post(self):
        try:
            api_key = request.headers.get("x-api-key")
            print(f"[DEBUG] Clé reçue : {api_key}")

            if not api_key:
                abort(400, description="La clé d'API est requise.")

            user = User.query.filter_by(api_key=api_key).first()
            print(f"[DEBUG] Utilisateur trouvé : {user}")

            if user:
                return {
                    "message": "Authentification réussie",
                    "user_email": user.email
                }, 200
            else:
                abort(401, description="Clé d'API invalide.")

        except Exception as e:
            print(f"[ERROR] Erreur serveur dans /authenticate : {e}")
            return {"message": "Erreur interne du serveur."}, 500
