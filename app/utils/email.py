# app/utils/email.py
import os
import smtplib
from email.message import EmailMessage

from celery import Celery

# Récupère le mot de passe et l'adresse email depuis les variables d'environnement
APP_EMAIL = os.environ.get("APP_EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")

def send_email(to: str, subject: str, body: str, attachment: bytes = None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = APP_EMAIL  # Utilise l'email depuis le .env
    msg["To"] = to
    msg.set_content(body)
    
    if attachment:
        # Ajout de l'image du QR Code en pièce jointe
        msg.add_attachment(attachment, maintype="image", subtype="png", filename="qrcode.png")
    
    # Connexion au serveur SMTP et envoi de l'email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
            server.ehlo()
            server.starttls()  # Active le chiffrement TLS
            server.ehlo()
            # Se connecter avec les identifiants Gmail ou avec un mot de passe d'application
            server.login(APP_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print("Email envoyé avec succès.")
    except Exception as e:
        print("Erreur lors de l'envoi de l'email :", e)


