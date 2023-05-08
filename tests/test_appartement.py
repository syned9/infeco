from tests.conftest import client
from app import db
from app.models import Appartement

class TestAppartement:
    def test_create_appartement(self):
        # test pour créer un appartement
        appartement = Appartement(adresse="Ker Anne", complement="",
                                   ville="Saint Père en retz", code_postal="44320", loyer=2000,
                                   charges=230, depot_garantie=4000)
        db.session.add(appartement)
        db.session.commit()
        assert appartement.id is not None
        
    def test_modify_appartement(self):
        # test pour modifier les prix d'un appartement
        appartement = Appartement(adresse="Ker Anne", complement="",
                                   ville="Saint Père en retz", code_postal="44320", loyer=2000,
                                   charges=230, depot_garantie=4000)
        db.session.add(appartement)
        db.session.commit()
        appartement.loyer = 2300
        db.session.commit()
        assert appartement.loyer == 2300

    def test_delete_appartement(self):
        # Créer un nouvel appartement
        appartement = Appartement(adresse="Ker Anne", complement="",
                                   ville="Saint Père en retz", code_postal="44320", loyer=2000,
                                   charges=230, depot_garantie=4000)
        db.session.add(appartement)
        db.session.commit()

        # Vérifier que l'appartement a été ajouté à la base de données
        assert Appartement.query.count() == 1

        # Supprimer l'appartement de la base de données
        db.session.delete(appartement)
        db.session.commit()

        # Vérifier que l'appartement a été supprimé de la base de données
        assert Appartement.query.count() == 0