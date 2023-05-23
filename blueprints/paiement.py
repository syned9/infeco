from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.forms import PaiementForm
from app.models import Paiement, TypePaiement, Contrat
from app import db
from sqlalchemy.orm import joinedload
from flask_security import login_required

paiement_bp = Blueprint('paiement_bp', __name__)

@paiement_bp.route('/paiement')
@login_required
def index():
    # Select all paiements in BDD
    paiements = db.session.query(Paiement).all()
    for paiement in paiements:
        # Charger les relations pour éviter les requêtes supplémentaires
        db.session.query(Paiement).options(joinedload(Paiement.type_paiement), joinedload(Paiement.contrat)).filter(Paiement.id == paiement.id)
    # Trier les paiements par date
    paiements_tries = sorted(paiements, key=lambda x: x.date, reverse=True)
    return render_template('paiement/index.html', title='Liste paiements', paiements=paiements_tries, nb_paiements=len(paiements_tries))

@paiement_bp.route('/paiement/add', methods=['get', 'post'])
@login_required
def add():
    try:
        type_paiements = db.session.query(TypePaiement).all()
        contrats = db.session.query(Contrat).all()
        # Trier les contrats par libelle
        contrats_tries = sorted(contrats, key=lambda x: x.libelle)
        # Trier les type_paiements par libelle
        type_paiements_tries = sorted(type_paiements, key=lambda x: x.libelle)
        form = PaiementForm()
        form.type_paiement_id.choices = [(type_paiement.id, type_paiement.libelle) for type_paiement in type_paiements_tries]
        form.contrat_id.choices = [(contrat.id, contrat.libelle) for contrat in contrats_tries]
        if form.validate_on_submit():
            # Insert paiement in BDD
            paiement = Paiement(libelle=form.libelle.data, date=form.date.data, montant=form.montant.data,
                                origine=int(form.origine.data), type_paiement_id=form.type_paiement_id.data, 
                                contrat_id=form.contrat_id.data)
            db.session.add(paiement)
            db.session.commit()
            # Message flash ok
            flash('Le paiement a bien été enregistrer', 'success')
            return redirect(url_for('paiement_bp.index'))
        return render_template('paiement/add.html', form=form, title='Ajouter un paiement', route='paiement_bp')
    except Exception:
        flash('Erreur, un problème est survenu lors de l\'ajout d\'un paiement', 'danger')
        return redirect(url_for('paiement_bp.index'))

@paiement_bp.route('/paiement/edit/<int:id>', methods=['get', 'post'])
@login_required
def edit(id):
    try:
        # Select paiement in BDD
        paiement = db.session.get(Paiement, id)
        type_paiements = db.session.query(TypePaiement).all()
        contrats = db.session.query(Contrat).all()
        # Trier les contrats par libelle
        contrats_tries = sorted(contrats, key=lambda x: x.libelle)
        # Trier les type_paiements par libelle
        type_paiements_tries = sorted(type_paiements, key=lambda x: x.libelle)
        if request.method == 'GET':
            if paiement.origine:
                paiement.origine = 1
            else:
                paiement.origine = 0
            form = PaiementForm(obj=paiement)
        else:
            form = PaiementForm()
        form.type_paiement_id.choices = [(type_paiement.id, type_paiement.libelle) for type_paiement in type_paiements_tries]
        form.contrat_id.choices = [(contrat.id, contrat.libelle) for contrat in contrats_tries]
        if form.validate_on_submit():
            # Update paiement in BDD
            paiement.date = form.date.data
            paiement.origine = int(form.origine.data)
            paiement.montant = form.montant.data
            paiement.libelle = form.libelle.data
            paiement.type_paiement_id = form.type_paiement_id.data
            paiement.contrat_id = form.contrat_id.data
            db.session.commit()
            # Message flash ok
            flash('Le paiement a bien été modifié', 'success')
            return redirect(url_for('paiement_bp.index'))
        return render_template('paiement/add.html', form=form, title='Modifier un paiement', route='paiement_bp')
    except Exception:
        flash('Erreur, un problème est survenu lors de la modification du paiement', 'danger')
        return redirect(url_for('paiement_bp.index'))

@paiement_bp.route('/paiement/del/<int:id>', methods=['get', 'post'])
@login_required
def delete(id):
    try:
        # Select paiement in BDD
        paiement = db.session.get(Paiement, id)
        # Delete paiement in BDD
        db.session.delete(paiement)
        db.session.commit()
        # Message flash ok
        flash('Le paiement a bien été supprimé', 'success')
        return redirect(url_for('paiement_bp.index'))
    except Exception:
        flash('Erreur, un problème est survenu lors de la suppression du paiement', 'danger')
        return redirect(url_for('paiement_bp.index'))