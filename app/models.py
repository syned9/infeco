from app import db

class Appartement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adresse = db.Column(db.String(255), nullable=False)
    complement = db.Column(db.String(255))
    ville = db.Column(db.String(100), nullable=False)
    code_postal = db.Column(db.String(10), nullable=False)
    loyer = db.Column(db.Float, nullable=False)
    charges = db.Column(db.Float, nullable=False)
    depot_garantie = db.Column(db.Float, nullable=False)

    def __init__(self, adresse, complement, ville, code_postal, loyer, charges, depot_garantie):
        self.adresse = adresse
        self.complement = complement
        self.ville = ville
        self.code_postal = code_postal
        self.loyer = loyer
        self.charges = charges
        self.depot_garantie = depot_garantie

    def __repr__(self):
        return '<Appartement %r>' % self.adresse



class EtatDesLieux(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Locataire(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Paiement(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Contrat(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Agence(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class TypePaiement(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Quittance(db.Model):
    id = db.Column(db.Integer, primary_key=True)

