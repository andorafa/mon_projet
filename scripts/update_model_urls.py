import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Product

app = create_app()

with app.app_context():
    # Récupérer les produits un par un
    p1 = Product.query.get(5)
    p2 = Product.query.get(6)

    update = False  # Un flag pour savoir si on doit commit ou non

    if p1:
        p1.model_url = "https://drive.google.com/uc?export=download&id=1Oq_vVepdhZqbhX2Gm7nVcQqttLrlwZWQ"
        print("✅ model_url mis à jour pour le produit 5.")
        update = True
    else:
        print("⚠️ Produit 5 introuvable en base.")

    if p2:
        p2.model_url = "https://drive.google.com/uc?export=download&id=1PsD-QhE0z1R-v4mcY8-W0CFw746oLUXl"
        print("✅ model_url mis à jour pour le produit 6.")
        update = True
    else:
        print("⚠️ Produit 6 introuvable en base.")

    if update:
        db.session.commit()
        print("✅ Les mises à jour ont été enregistrées.")
    else:
        print("⚠️ Aucun produit mis à jour, rien n’a été enregistré.")
