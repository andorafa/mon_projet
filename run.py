from app import create_app, db

app = create_app()

# 📦 Assurer la création des tables si besoin (en local/dev uniquement)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
