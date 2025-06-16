from flask_restx import Namespace, Resource
from app import db

ns = Namespace("admin", description="Admin DB")

@ns.route("/init-db")
class InitDBAPI(Resource):
    def post(self):
        db.create_all()
        return {"message": "✅ Base de données initialisée avec succès."}, 200
