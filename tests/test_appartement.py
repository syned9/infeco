import pytest
from app import db
from tests.conftest import client
from app.models import Appartement

# class TestFonctionnelAppartement():

#     def test_should_status_code_ok(self, client):
#         client.post('/appartement/add', data={'adresse' : 'ker anne 2', 'complement' : '', 'ville' : 'Saint Père en retz 2', 'code_postal' : '44000', 'loyer' : 988, 'charge' : 123, 'depot_garantie' : 2300, 'agence_id' : 2})
#         # response = client.get('/appartement/add')
# 	    # data = response.data.decode() #Permet de décoder la data dans la requête
#         # assert data == 1

@pytest.mark.usefixtures('new_appartement')
class TestAppartement():

    def test_create_appartement(self, new_appartement):
        # test pour créer un appartement
        assert new_appartement.id is not None
        assert new_appartement.adresse == 'Ker Anne'
        assert new_appartement.complement == ''
        assert new_appartement.ville == 'Saint Père en retz'
        assert new_appartement.code_postal == '44320'
        assert new_appartement.loyer == 2000
        assert new_appartement.charges == 230
        assert new_appartement.depot_garantie == 4000
        assert new_appartement.agence_id == 1

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