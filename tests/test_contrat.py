import pytest
from app import db
from app.models import Contrat
from datetime import datetime

@pytest.mark.usefixtures('new_contrat')
class TestContrat:
    def test_create_contrat(self, new_contrat):
        assert new_contrat.id is not None
        assert new_contrat.date_debut == datetime(year=2023, month=3, day=17)
        assert new_contrat.date_fin == datetime(year=2024, month=6, day=30)
        assert new_contrat.locataire_id == 1
        assert new_contrat.appartement_id == 1

    def test_update_contrat(self, new_contrat):
        new_contrat.date_debut = datetime(year=2023, month=8, day=17)
        db.session.commit()
        updated_contrat = Contrat.query.get(new_contrat.id)
        assert updated_contrat.date_debut == datetime(year=2023, month=8, day=17)

    def test_delete_contrat(self, new_contrat):
        db.session.delete(new_contrat)
        db.session.commit()
        deleted_contrat = Contrat.query.get(new_contrat.id)
        assert deleted_contrat is None