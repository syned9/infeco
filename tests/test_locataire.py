import pytest
from app import db
from app.models import Locataire

@pytest.mark.usefixtures('new_locataire')
class TestLocataire():

    def test_create_locataire(self, new_locataire):
        assert new_locataire.id is not None
        assert new_locataire.nom == "Navarro"
        assert new_locataire.prenom == "Robin"
        assert new_locataire.telephone == "0789742300"
        assert new_locataire.email == "robin.navarro@example.com"

    def test_update_nom(self, new_locataire):
        new_locataire.nom = 'Perron'
        db.session.commit()
        updated_locataire = Locataire.query.get(new_locataire.id)
        assert updated_locataire.nom == 'Perron'

    def test_delete_locataire(self, new_locataire):
        db.session.delete(new_locataire)
        db.session.commit()
        deleted_locataire = Locataire.query.get(new_locataire.id)
        assert deleted_locataire == None