
import os


USE_MOCK_PRODUCTS = os.getenv("USE_MOCK_PRODUCTS", "false").lower() == "true"

import uuid
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
    def _create_user(email="test@example.com", api_key=None):
        if not api_key:
            api_key = str(uuid.uuid4())

        with app.app_context():
            db.session.query(User).filter_by(email=email).delete()
            db.session.query(User).filter_by(api_key=api_key).delete()
            db.session.commit()

            user = User(email=email, api_key=api_key)
            db.session.add(user)
            db.session.commit()
            return user

    return _create_user

