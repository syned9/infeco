import pytest
from app import db
from app.models import TypePaiement

@pytest.mark.usefixtures('new_typePaiement')
class TestTypePaiement:

    def test_create_type_paiement(self, new_typePaiement):
        assert new_typePaiement.id is not None
        assert new_typePaiement.libelle == "Loyer"

    def test_update_type_paiement(new_typePaiement):
        new_typePaiement.libelle = "Dépot de garantie"
        db.session.commit()
        updated_type_paiement = TypePaiement.query.filter_by(id=new_typePaiement.id).first()
        assert updated_type_paiement.libelle == "Dépot de garantie"

    def test_delete_type_paiement(new_typePaiement):
        db.session.delete(new_typePaiement)
        db.session.commit()
        deleted_type_paiement = TypePaiement.query.filter_by(id=new_typePaiement.id).first()
        assert deleted_type_paiement is None