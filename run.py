from flask import Flask
from app import create_app, db

app = create_app()

# ➕ Route pour vérifier que l'API est vivante
@app.route("/")
def index():
    return "✅ API is running", 200

# Assurer que les tables sont créées (utile en local/dev)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
