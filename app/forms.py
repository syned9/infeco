from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SelectField, TextAreaField, DateField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email

class AppartementForm(FlaskForm):
    libelle = StringField('Libellé', validators=[DataRequired()])
    adresse = StringField('Adresse', validators=[DataRequired()])
    complement = StringField('Complement d\'adresse', validators=[])
    ville = StringField('Ville', validators=[DataRequired()])
    code_postal = StringField('Code postal', validators=[DataRequired()])
    loyer = DecimalField('Loyer', validators=[DataRequired()])
    charges = DecimalField('Charges', validators=[DataRequired()])
    depot_garantie = DecimalField('Dépot de garantie', validators=[DataRequired()])
    submit = SubmitField('Valider')

class LocataireForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    telephone = StringField('Téléphone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Valider')

class PaiementForm(FlaskForm):
    libelle = StringField('Libellé', validators=[DataRequired()])
    date = DateField('Date du paiement', validators=[DataRequired()])
    montant =  DecimalField('Montant', validators=[DataRequired()])
    origine = RadioField('Origine du paiement', choices=[(0, 'locataire'), (1, 'caisse d\'allocation familiale')], validators=[DataRequired()])
    type_paiement_id = SelectField('Type de paiement', choices=[], validators=[DataRequired()])
    contrat_id = SelectField('Contrat', choices=[], validators=[DataRequired()])
    submit = SubmitField('Valider')

class ContratForm(FlaskForm):
    libelle = StringField('Libellé', validators=[DataRequired()])
    date_debut = DateField('Date debut de contrat', validators=[DataRequired()])
    date_fin = DateField('Date fin de contrat', validators=[DataRequired()])
    locataire_id = SelectField('Locataire', choices=[], validators=[DataRequired()])
    appartement_id = SelectField('Appartement', choices=[], validators=[DataRequired()])
    montant =  DecimalField('Montant', validators=[DataRequired()])
    submit = SubmitField('Valider')

class EtatLieuxForm(FlaskForm):
    date = DateField('Date de L\'état des lieux', validators=[DataRequired()])
    remarque = TextAreaField('Remarques', validators=[])
    situation = RadioField('Situation', choices=[(0, 'Entré'), (1, 'Sorti')], validators=[DataRequired()])
    contrat_id = SelectField('Contrat', choices=[])
    submit = SubmitField('Valider')

class QuittanceForm(FlaskForm):
    date_debut = DateField('Date debut de la quittance', validators=[DataRequired()])
    date_fin = DateField('Date fin de la quittance', validators=[DataRequired()])
    submit = SubmitField('Générer')

class UserForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    role = SelectField('Role', choices=[], validators=[DataRequired()])
    submit = SubmitField('Créer')

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()], render_kw={"placeholder": "Nom d'utilisateur"}) 
    password = PasswordField('Mot de passe', validators=[DataRequired()], render_kw={"placeholder": "Mot de passe"})
    # remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')


