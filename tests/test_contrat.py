import pytest
from app import db
from app.models import Contrat

@pytest.mark.usefixtures('new_contrat')
class TestContrat:
    def test_create_contrat(self, new_contrat):
        assert new_contrat.id is not None

    def test_update_contrat(self, new_contrat):
        new_contrat.date_debut = '2023-08-17'
        db.session.commit()
        updated_contrat = Contrat.query.get(new_contrat.id)
        assert updated_contrat.date_debut == '2023-08-17'

    def test_delete_contrat(self, new_contrat):
        db.session.delete(new_contrat)
        db.session.commit()
        deleted_contrat = Contrat.query.get(new_contrat.id)
        assert deleted_contrat is None