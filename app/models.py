from app import db
from datetime import datetime, date
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text, Date
from sqlalchemy.orm import relationship

class Appartement(db.Model):
    __tablename__ = 'appartement'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    adresse = Column(String(255), nullable=False)
    complement = Column(String(255))
    ville = Column(String(100), nullable=False)
    code_postal = Column(String(10), nullable=False)
    loyer = Column(Float, nullable=False)
    charges = Column(Float, nullable=False)
    libelle = Column(String(100), nullable=False)
    depot_garantie = Column(Float, nullable=False)
    agence_id = Column(Integer, ForeignKey('agence.id'))
    agence = relationship('Agence', back_populates='appartements')
    contrats = relationship('Contrat', back_populates='appartement')


    def __init__(self, libelle: str, adresse: str, complement: str, ville: str, code_postal: str, loyer: float, charges: float, depot_garantie: float, agence_id: int):
        self.libelle = libelle
        self.adresse = adresse
        self.complement = complement
        self.ville = ville
        self.code_postal = code_postal
        self.loyer = loyer
        self.charges = charges
        self.depot_garantie = depot_garantie
        self.agence_id = agence_id

    def __repr__(self):
        return '<Appartement %r>' % self.adresse

class Agence(db.Model):
    __tablename__ = 'agence'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(255), nullable=False)
    prelevement = Column(Float, nullable=False)
    appartements = relationship('Appartement', back_populates='agence')

    def __init__(self, nom: str, prelevement: str = None):
        self.nom = nom
        self.prelevement = prelevement

    def __repr__(self):
        return f"<Agence(id='{self.id}', nom='{self.nom}', prelevement='{self.prelevement}')>"

class Locataire(db.Model):
    __tablename__ = 'locataire'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(50))
    prenom = Column(String(50))
    telephone = Column(String(20))
    email = Column(String(50))
    contrats = relationship('Contrat', back_populates='locataire')
    quittances = relationship("Quittance", back_populates='locataire')

    def __init__(self, nom: str, prenom: str, telephone: str, email: str):
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.email = email

    def __repr__(self):
        return f"<Locataire {self.nom} {self.prenom}>"

class Paiement(db.Model):
    __tablename__ = 'paiement'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow)
    montant = Column(Float)
    origine = Column(Boolean)
    libelle = Column(String(100), nullable=False)
    type_paiement_id = Column(Integer, ForeignKey('type_paiement.id'))
    type_paiement = relationship('TypePaiement', back_populates='paiements')
    contrat_id = Column(Integer, ForeignKey('contrat.id'))
    contrat = relationship('Contrat', back_populates='paiements')

    def __init__(self, libelle: str, date: datetime, montant: float, origine: bool, type_paiement_id: int, contrat_id: int):
        self.libelle = libelle
        self.date = date
        self.montant = montant
        self.origine = origine
        self.type_paiement_id = type_paiement_id
        self.contrat_id = contrat_id

    def __repr__(self):
        return f"<Paiement {self.date} {self.montant}>"

class TypePaiement(db.Model):
    __tablename__ = 'type_paiement'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    libelle = Column(String(255), nullable=False)

    paiements = relationship("Paiement", back_populates="type_paiement")

    def __init__(self, libelle: str):
        self.libelle = libelle

    def __repr__(self):
        return f"<TypePaiement(id='{self.id}', libelle='{self.libelle}')>"

class Contrat(db.Model):
    __tablename__ = 'contrat'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    libelle = Column(String(100), nullable=False)
    date_debut = Column(Date)
    date_fin = Column(Date)
    locataire_id = Column(Integer, ForeignKey('locataire.id'))
    locataire = relationship('Locataire', back_populates='contrats')
    appartement_id = Column(Integer, ForeignKey('appartement.id'))
    appartement = relationship('Appartement', back_populates='contrats')
    paiements = relationship('Paiement', back_populates='contrat')
    etats_lieux = relationship("EtatLieux", back_populates="contrat")

    def __init__(self, libelle: str, date_debut: date, date_fin: date, locataire_id: int, appartement_id: int):
        self.libelle = libelle
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.locataire_id = locataire_id
        self.appartement_id = appartement_id

    def __repr__(self):
        return f"<Contrat(id='{self.id}', date_debut='{self.date_debut}', date_fin='{self.date_fin}')>"

class EtatLieux(db.Model):
    __tablename__ = 'etat_lieux'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DateTime, default=datetime.now)
    remarque = Column(Text)
    situation = Column(Boolean)
    contrat_id = Column(Integer, ForeignKey("contrat.id"))
    contrat = relationship("Contrat", back_populates="etats_lieux")

    def __init__(self, date: datetime, remarque: Text, situation: bool, contrat_id: int):
        self.date = date
        self.remarque = remarque
        self.situation = situation
        self.contrat_id = contrat_id

    def __repr__(self):
        return f"<EtatLieux {self.date}, {self.situation}, {self.contrat}>"

class Quittance(db.Model):
    __tablename__ = 'quittance'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    montant = Column(Float, nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)
    locataire_id = Column(Integer, ForeignKey('locataire.id'), nullable=False)
    locataire = relationship("Locataire", back_populates="quittances")
    
    def __init__(self, date_debut: datetime, date_fin: datetime, montant: float, date_creation: datetime, locataire_id: int):
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.montant = montant
        self.date_creation = date_creation
        self.locataire_id = locataire_id
    
    def __repr__(self):
        return f'<Quittance {self.id}>'


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    user_roles = relationship('UserRole', back_populates='role', cascade='all, delete-orphan')



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255))
    active = Column(Boolean)
    user_roles = relationship('UserRole', back_populates='user', cascade='all, delete-orphan')

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    user = relationship('User', back_populates='user_roles')
    role = relationship('Role', back_populates='user_roles')