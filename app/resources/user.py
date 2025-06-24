from flask_restx import Namespace, Resource, reqparse, fields
from app.models import User
from app import db
import uuid, io, base64, qrcode
from app.utils.email import send_email

ns = Namespace("users", description="Création d'utilisateur")

user_model = ns.model("User", {
    "email": fields.String(required=True),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True)
})

@ns.route("")
class UserAPI(Resource):
    @ns.expect(user_model)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True)
        parser.add_argument("first_name", type=str, required=True)
        parser.add_argument("last_name", type=str, required=True)
        args = parser.parse_args()
        email = args["email"]
        first_name = args["first_name"]
        last_name = args["last_name"]

        user = User.query.filter_by(email=email).first()
        user_key = str(uuid.uuid4())
        if user:
            user.api_key = user_key
            user.first_name = first_name
            user.last_name = last_name
        else:
            user = User(email=email, api_key=user_key, first_name=first_name, last_name=last_name)
            db.session.add(user)
        db.session.commit()

        qr = qrcode.QRCode()
        qr.add_data(user_key)
        img = qr.make_image(fill='black', back_color='white')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        byte_im = buf.getvalue()
        encoded_img = base64.b64encode(byte_im).decode('utf-8')
        send_email(to=email, subject="QR Code", body="Voici votre clé", attachment=byte_im)

        return {"message": "Utilisateur connecté", "api_key": user_key, "qr_code": encoded_img}, 201
