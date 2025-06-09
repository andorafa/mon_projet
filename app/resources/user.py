from flask_restful import Resource, reqparse
from app.models import User
from app import db
import uuid
import io
import base64
import qrcode
from app.utils.email import send_email

class UserAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="L'email est obligatoire.")
        args = parser.parse_args()
        email = args['email']







        # Recherche ou création de l'utilisateur


        user = User.query.filter_by(email=email).first()


        if user:


            # Régénère une nouvelle clé pour reconnexion


            user_key = str(uuid.uuid4())


            user.api_key = user_key


        else:


            # Création d'un nouvel utilisateur


            user_key = str(uuid.uuid4())


            user = User(email=email, api_key=user_key)


            db.session.add(user)





        db.session.commit()





        # Générer et encoder le QR Code


        qr = qrcode.QRCode(version=1, box_size=10, border=5)


        qr.add_data(user_key)


        qr.make(fit=True)


        img = qr.make_image(fill='black', back_color='white')


        buf = io.BytesIO()


        img.save(buf, format='PNG')


        byte_im = buf.getvalue()


        encoded_img = base64.b64encode(byte_im).decode('utf-8')





        # Envoi de l'email


        send_email(


            to=email,


            subject="Votre QR Code",


            body="Voici votre QR Code pour accéder à l'application mobile.",


            attachment=byte_im


        )





        return {


            "message": "Utilisateur (re)connecté avec succès",

            "api_key": user_key,

            "qr_code": encoded_img

        }, 201