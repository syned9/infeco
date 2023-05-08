import pytest
from app import db
from app.models import Paiement

@pytest.mark.usefixtures('new_paiement')
class TestPaiement():

    def test_create_paiement(self, new_paiement):
        assert new_paiement.id is not None
        assert new_paiement.date == '2023-06-16'
        assert new_paiement.montant == 900
        assert new_paiement.origine == 'locataire'
        assert new_paiement.type_paiement == 1

    def test_update_paiement(db, new_paiement):
        new_origine = "charges"
        new_paiement.origine = new_origine
        db.session.commit()
        updated_paiement = Paiement.query.get(new_paiement.id)
        assert updated_paiement.origine == new_origine

    def test_delete_paiement(db, new_paiement):
        paiement = new_paiement
        db.session.delete(paiement)
        db.session.commit()
        deleted_paiement = Paiement.query.get(paiement.id)
        assert deleted_paiement is None