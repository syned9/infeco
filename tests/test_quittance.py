from datetime import datetime
import pytest
from app import db
from app.models import Quittance

@pytest.mark.usefixtures('new_quittance')
class TestQuittance:
    def test_create_quittance(self, new_quittance):
        assert new_quittance.id is not None
        assert new_quittance.date_debut == datetime.date.today()
        assert new_quittance.date_fin == datetime.date.today() + datetime.timedelta(days=30)
        assert new_quittance.montant == 900
        assert new_quittance.date_creation is not None

    # def test_update_quittance(self, new_quittance):
    #     new_quittance.montant = 790
    #     db.session.commit()
    #     assert new_quittance.montant == 790

    def test_delete_quittance(self, new_quittance):
        db.session.delete(new_quittance)
        db.session.commit()
        assert Quittance.query.get(new_quittance.id) is None