from app import db,create_app
from app.models import TypePaiement
from instance.config import DevelopmentConfig, ProductionConfig, TestingConfig
import os

app = create_app(ProductionConfig)

with app.app_context():
        db.create_all()
        # Vérifier si les types de paiement existent déjà
        if not TypePaiement.query.filter_by(libelle='loyer').first():
                # ajout des types de paiement
                typePaiement = TypePaiement(libelle='loyer')
                db.session.add(typePaiement)
                
        if not TypePaiement.query.filter_by(libelle='charges').first():
                typePaiement2 = TypePaiement(libelle='charges')
                db.session.add(typePaiement2)
                
        if not TypePaiement.query.filter_by(libelle='dépôt de garantie').first():
                typePaiement3 = TypePaiement(libelle='dépôt de garantie')
                db.session.add(typePaiement3)

        db.session.commit()

if __name__ == '__main__':
    app.run(port=os.environ.get('PORT', 5000))