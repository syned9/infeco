import pytest
from app import create_app, db
from instance.config import TestingConfig
from app.models import Appartement

@pytest.fixture(scope='module')
def test_db():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        # db.drop_all()

@pytest.fixture(scope='function')
def new_appartement(test_db):
    appartement = Appartement(adresse="Ker Anne", complement="",
                                   ville="Saint Père en retz", code_postal="44320", loyer=2000,
                                   charges=230, depot_garantie=4000)
    test_db.session.add(appartement)
    test_db.session.commit()
    yield appartement
    test_db.session.delete(appartement)
    test_db.session.commit()
