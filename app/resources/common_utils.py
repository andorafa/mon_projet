# ✅ Factorisation commune pour webshop, revendeurs, crm
# 📁 app/resources/common_utils.py

def parse_mock_product(p):
    price_str = str(p.get("details", {}).get("price", "0")).replace(',', '.')
    return {
        "id": int(p["id"]),
        "name": p["name"],
        "description": p.get("details", {}).get("description", ""),
        "price": float(price_str),
        "model_url": "",
        "created_at": p.get("createdAt", ""),
        "stock": int(p.get("stock", 0)) if isinstance(p.get("stock", 0), int) else 0,
    }

def validate_api_key(provided_key, expected_key):
    if not provided_key or provided_key != expected_key:
        from flask import abort
        abort(401, description="Clé API invalide ou manquante")
