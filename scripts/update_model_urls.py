

import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app import create_app, db
from app.models import Product

app = create_app()

with app.app_context():
    p1 = Product.query.get(5)
    p2 = Product.query.get(6)

    if p1 and p2:
        p1.model_url = "https://drive.google.com/uc?export=download&id=1Oq_vVepdhZqbhX2Gm7nVcQqttLrlwZWQ"
        p2.model_url = "https://drive.google.com/uc?export=download&id=1PsD-QhE0z1R-v4mcY8-W0CFw746oLUXl"
        db.session.commit()
        print("✅ URLs model_url mises à jour pour les produits 5 et 6.")
    else:
        print("⚠️ Un ou les deux produits n'ont pas été trouvés en base.")
