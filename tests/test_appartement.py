import pytest
from app import db
from app.models import Appartement

@pytest.mark.usefixtures('new_appartement')
class TestAppartement():



    def test_create_appartement(self, new_appartement):
        # test pour créer un appartement
        assert new_appartement.id is not None

    def test_modify_appartement(self, new_appartement):
        # test pour modifier appartement les prix d'un appartement
        new_appartement.loyer = 2300
        db.session.commit()
        assert new_appartement.loyer == 2300

    def test_delete_appartement(self, new_appartement):
        # Vérifier que l'appartement a été ajouté à la base de données
        assert Appartement.query.count() == 1

        # Supprimer l'appartement de la base de données
        db.session.delete(new_appartement)
        db.session.commit()

        # Vérifier que l'appartement a été supprimé de la base de données
        assert Appartement.query.count() == 0