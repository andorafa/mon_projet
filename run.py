# run.py
from flask import redirect
from app import create_app, db

app = create_app()


@app.route("/swagger")
def index():
    return redirect('/swagger')

# 📦 Assurer la création des tables si besoin (en local/dev uniquement)
with app.app_context():
    db.create_all()

if __name__ == "__creation-apirest__":
    app.run(host="0.0.0.0", port=5000)
