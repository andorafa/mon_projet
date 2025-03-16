import io
import base64
import uuid
import qrcode
from flask_restful import Resource, reqparse
from app import db
from app.models import User
from app.utils.email import send_email

class UserAPI(Resource):
    def post(self):
        # Parser pour récupérer l'email dans le corps de la requête JSON
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="L'email est obligatoire.")
        args = parser.parse_args()
        email = args['email']

        # Générer une clé unique (ici avec uuid4)
        user_key = str(uuid.uuid4())

        # Création d'un nouvel utilisateur
        new_user = User(email=email, api_key=user_key)
        db.session.add(new_user)
        db.session.commit()

        # Générer le QR Code pour la clé d'authentification
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(user_key)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        
        # Sauvegarder l'image du QR Code en mémoire
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        byte_im = buf.getvalue()

        # Encodage en base64 pour faciliter le transfert via JSON
        encoded_img = base64.b64encode(byte_im).decode('utf-8')


        send_email(
            to=email,
            subject="Votre QR Code",
            body="Voici votre QR Code pour accéder à l'application mobile.",
            attachment=byte_im
        )

        return {
            "message": "Utilisateur créé avec succès",
            "api_key": user_key,
            "qr_code": encoded_img  # Ce champ contient l'image du QR Code encodée en base64
        }, 201
