import pytest
from app import create_app, db
from instance.config import TestingConfig


@pytest.fixture
def client(classe):
    app = create_app(TestingConfig)
    classe.app_context = classe.app.app_context()
    classe.app_context.push()
    db.create_all()
    with app.test_client() as client:
        yield client

def teardown_class(classe):
        # nettoyage après les tests
        db.session.remove()
        db.drop_all()
        classe.app_context.pop()
