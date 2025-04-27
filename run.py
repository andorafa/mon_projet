# run.py
import os
import sys

# Ajout du chemin pour GitHub Actions si besoin
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == "__main__":
    print("🚀 Flask server starting on 0.0.0.0:5000...")
    app.run(host="0.0.0.0", port=5000)

