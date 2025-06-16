import pytest
from app import create_app, db
from app.models import User

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture
def setup_user(app):
    with app.app_context():
        db.session.query(User).delete()
        db.session.add(User(email="test@webshop.com", api_key="webshop123"))
        db.session.commit()
