from app import db,create_app
from app.models import TypePaiement, Role, Agence
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

        if not Role.query.filter_by(name='utilisateur').first():
                role = Role(name='utilisateur')
                db.session.add(role)

        if not Agence.query.filter_by(nom='Agence 1').first():
                agence = Agence(nom='Agence 1', prelevement=8)
                db.session.add(agence)

        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=os.environ.get('PORT', 5000))