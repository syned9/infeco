import pytest
from app import db
from app.models import Agence

@pytest.mark.usefixtures('new_agence')
class TestAgence:
    def test_create_agence(self, new_agence):
        assert new_agence.id is not None
        assert new_agence.nom == 'Agence 1'
        assert new_agence.prelevement == 8

    def test_update_agence(self, new_agence):
        new_agence.nom = 'Agence 2'
        db.session.commit()
        agence = Agence.query.get(new_agence.id)
        assert agence.nom == 'Agence 2'

    def test_delete_agence(self, new_agence):
        db.session.delete(new_agence)
        db.session.commit()
        agence = Agence.query.get(new_agence.id)
        assert agence is None