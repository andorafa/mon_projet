from app.models import Product, User

def test_product_repr():
    product = Product(name="Test", description="", price=1.0, model_url="")
    assert repr(product) == "<Product Test>"

def test_user_repr():
    user = User(email="toto@test.com", api_key="xyz")
    assert repr(user) == "<User toto@test.com>"
