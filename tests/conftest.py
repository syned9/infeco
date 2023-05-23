from datetime import datetime, timedelta
import pytest
from app import create_app, db
from instance.config import TestingConfig
from app.models import Appartement, EtatLieux, Locataire, Paiement, Contrat, Agence, TypePaiement, Quittance

@pytest.fixture(scope='module')
def client():    
    app = create_app(TestingConfig)
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def test_db():
    app = create_app(TestingConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def new_appartement(test_db):
    appartement = Appartement(libelle="appartement 1", adresse="Ker Anne", complement="",
                                   ville="Saint Père en retz", code_postal="44320", loyer=2000,
                                   charges=230, depot_garantie=4000, agence_id=1)
    test_db.session.add(appartement)
    test_db.session.commit()
    yield appartement
    test_db.session.delete(appartement)
    test_db.session.commit()

@pytest.fixture(scope='function')
def new_EtatLieux(test_db):
    edl = EtatLieux(date='2023-02-12', remarque='Propre', situation=0, contrat_id=1)
    test_db.session.add(edl)
    test_db.session.commit()
    yield edl
    test_db.session.delete(edl)
    test_db.session.commit()

@pytest.fixture(scope='function')
def new_locataire(test_db):
    locataire = Locataire(nom='Navarro', prenom='Robin', telephone='0789742300', email='robin.navarro@example.com')
    test_db.session.add(locataire)
    test_db.session.commit()
    yield locataire
    test_db.session.delete(locataire)
    test_db.session.commit()

@pytest.fixture(scope='function')
def new_paiement(test_db):
     # Créer un nouvel objet Paiement
    paiement = Paiement(libelle="paiement 1", date='2023-06-16', montant=900, origine=0, type_paiement_id=1, contrat_id=1)
    # Ajouter le nouvel objet à la base de données pour le test
    test_db.session.add(paiement)
    test_db.session.commit()
    # Renvoyer l'objet Paiement créé pour les tests
    yield paiement
    # Nettoyer la base de données après les tests
    test_db.session.delete(paiement)
    test_db.session.commit()

@pytest.fixture(scope='function')
def new_contrat(test_db):
     # Créer un nouvel objet Contrat
    contrat = Contrat(libelle="contrat 1", date_debut='2023-03-17', date_fin='2024-06-30', locataire_id=1, appartement_id=1)    
    # Ajouter le nouvel objet à la base de données pour le test
    test_db.session.add(contrat)
    test_db.session.commit()
    # Renvoyer l'objet contrat créé pour les tests
    yield contrat
    # Nettoyer la base de données après les tests
    test_db.session.delete(contrat)
    test_db.session.commit()

@pytest.fixture(scope='function')
def new_agence(test_db):
     # Créer un nouvel objet Agence
    agence = Agence(nom='Agence 1', prelevement='8')    
    # Ajouter le nouvel objet à la base de données pour le test
    test_db.session.add(agence)
    test_db.session.commit()
    # Renvoyer l'objet agence créé pour les tests
    yield agence
    # Nettoyer la base de données après les tests
    test_db.session.delete(agence)
    test_db.session.commit()

@pytest.fixture(scope='function')
def new_typePaiement(test_db):
     # Créer un nouvel objet TypePaiement
    typePaiement = TypePaiement(libelle="Loyer")    
    # Ajouter le nouvel objet à la base de données pour le test
    test_db.session.add(typePaiement)
    test_db.session.commit()
    # Renvoyer l'objet typePaiement créé pour les tests
    yield typePaiement
    # Nettoyer la base de données après les tests
    test_db.session.delete(typePaiement)
    test_db.session.commit()

@pytest.fixture(scope='function')
def new_quittance(test_db):
     # Créer un nouvel objet Quittance
    quittance = Quittance(
        date_debut=datetime.today(),
        date_fin=datetime.today() + timedelta(days=30),
        montant=900,
        date_creation=datetime.now(),
        locataire_id=1
    )    # Ajouter le nouvel objet à la base de données pour le test
    test_db.session.add(quittance)
    test_db.session.commit()
    # Renvoyer l'objet quittance créé pour les tests
    yield quittance
    # Nettoyer la base de données après les tests
    test_db.session.delete(quittance)
    test_db.session.commit()
