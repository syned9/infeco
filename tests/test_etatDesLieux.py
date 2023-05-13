import pytest
from app import db
from app.models import EtatLieux
from datetime import datetime

@pytest.mark.usefixtures('new_EtatLieux')
class TestEtatLieux():

    def test_create_etat_des_lieux(self, new_EtatLieux):
        # Récupération de l'état des lieux depuis la base de données
        # edl_db = EtatLieux.query.filter_by(date='2023-02-12').first()

        # Vérification que les attributs de l'état des lieux correspondent bien à ceux définis lors de la création
        assert new_EtatLieux is not None
        assert new_EtatLieux.date == datetime(year=2023, month=2, day=12)
        assert new_EtatLieux.remarque == 'Propre'
        assert new_EtatLieux.situation == 0

    def test_update_etat_des_lieux(self, new_EtatLieux):
        # Modification de l'état des lieux
        new_EtatLieux.date = datetime(year=2022, month=6, day=1)
        new_EtatLieux.remarque = 'Nouvelle remarque'
        new_EtatLieux.situation = 1
        db.session.commit()

        # Récupération de l'état des lieux depuis la base de données
        edl_db = EtatLieux.query.filter_by(date='2022-06-01').first()

        # Vérification que les attributs de l'état des lieux ont bien été modifiés
        assert edl_db is not None
        assert edl_db.date == datetime(year=2022, month=6, day=1)
        assert edl_db.remarque == 'Nouvelle remarque'
        assert edl_db.situation == 1

    def test_delete_etat_des_lieux(self, new_EtatLieux):
        # Suppression de l'état des lieux
        db.session.delete(new_EtatLieux)
        db.session.commit()

        # Vérification que l'état des lieux n'existe plus dans la base de données
        edl_db = EtatLieux.query.filter_by(date='2023-02-12').first()
        assert edl_db is None