import pytest
from app import db
from app.models import EtatDesLieux

@pytest.mark.usefixtures('new_etatDesLieux')
class TestEtatDesLieux():

    def test_create_etat_des_lieux(self, new_etatDesLieux):
        # Récupération de l'état des lieux depuis la base de données
        edl_db = EtatDesLieux.query.filter_by(date='2023-02-12').first()

        # Vérification que les attributs de l'état des lieux correspondent bien à ceux définis lors de la création
        assert edl_db is not None
        assert edl_db.date == '2023-02-12'
        assert edl_db.remarque == 'Propre'
        assert edl_db.situation == 0

    def test_update_etat_des_lieux(self, new_etatDesLieux):
        # Modification de l'état des lieux
        new_etatDesLieux.date = '2022-06-01'
        new_etatDesLieux.remarque = 'Nouvelle remarque'
        new_etatDesLieux.situation = 1
        db.session.commit()

        # Récupération de l'état des lieux depuis la base de données
        edl_db = EtatDesLieux.query.filter_by(date='2022-06-01').first()

        # Vérification que les attributs de l'état des lieux ont bien été modifiés
        assert edl_db is not None
        assert edl_db.date == '2022-06-01'
        assert edl_db.remarque == 'Nouvelle remarque'
        assert edl_db.situation == 1

    def test_delete_etat_des_lieux(self, new_etatDesLieux):
        # Suppression de l'état des lieux
        db.session.delete(new_etatDesLieux)
        db.session.commit()

        # Vérification que l'état des lieux n'existe plus dans la base de données
        edl_db = EtatDesLieux.query.filter_by(date='2023-02-12').first()
        assert edl_db is None