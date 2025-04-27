# app/resources/init_db.py
from flask_restful import Resource
from app import db

class InitDBAPI(Resource):
    def post(self):
        db.create_all()
        return {"message": "✅ Base de données initialisée avec succès."}, 200
