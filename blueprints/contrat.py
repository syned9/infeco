from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.forms import ContratForm
from app.models import Contrat, Appartement, Locataire, Paiement
from datetime import date
from sqlalchemy import desc
from app import db
from flask_security import login_required


contrat_bp = Blueprint('contrat_bp', __name__)

@contrat_bp.route('/contrat')
@login_required
def index():
    # Select all contrats, appartements, locataires in BDD
    contrats = db.session.query(Contrat).all()
    appartements = db.session.query(Appartement).all()
    locataires = db.session.query(Locataire).all()

    # Trier les contrats par libelle
    contrats_tries = sorted(contrats, key=lambda x: x.libelle)
    data = []
    for contrat in contrats_tries:
        for appartement in appartements:
            if contrat.appartement_id == appartement.id:
                for locataire in locataires:
                    if contrat.locataire_id == locataire.id:
                        data.append({'contrat': contrat, 'appartement': appartement, 'locataire': locataire})
                        break
                break


    return render_template('contrat/index.html', title='Liste contrats', data=data, nb_contrats=len(contrats_tries))

@contrat_bp.route('/contrat/add', methods=['get', 'post'])
@login_required
def add():
    try:
        appartements = db.session.query(Appartement).all()
        locataires = db.session.query(Locataire).all()
        # Trier les appartements par libelle
        appartements_tries = sorted(appartements, key=lambda x: x.libelle)
        # Trier les locataires par nom
        locataires_tries = sorted(locataires, key=lambda x: x.nom)
        form = ContratForm()
        form.appartement_id.choices = [(appartement.id, appartement.libelle.upper() + ', ' + appartement.adresse) for appartement in appartements_tries]
        form.locataire_id.choices = [(locataire.id, locataire.nom + ' ' + locataire.prenom) for locataire in locataires_tries]
        if form.validate_on_submit():
            # Insert contrat in BDD
            contrat = Contrat(libelle=form.libelle.data, date_debut=form.date_debut.data, date_fin=form.date_fin.data, 
                                locataire_id=form.locataire_id.data, appartement_id=form.appartement_id.data) #, statut=0
            db.session.add(contrat)
            db.session.commit()
            # Message flash ok
            flash('Le contrat a bien été enregistrer', 'success')
            contrat_id = db.session.query(Contrat.id).order_by(desc(Contrat.id)).first()
            # Insert paiement in BDD
            paiement = Paiement(libelle='Dépot de garantie', date=date.today(), montant=form.montant.data,
                                origine=0, type_paiement_id=3, 
                                contrat_id=contrat_id[0])
            db.session.add(paiement)
            db.session.commit()
            # Message flash ok
            flash('Le dépôt de garantie a bien été validé', 'success')
            return redirect(url_for('contrat_bp.index'))
        return render_template('contrat/add.html', form=form, title='Ajouter un contrat', route='contrat_bp')
    except Exception:
        flash('Erreur, un problème est survenu lors de l\'ajout d\'un contrat', 'danger')
        return redirect(url_for('contrat_bp.index'))

@contrat_bp.route('/contrat/edit/<int:id>', methods=['get', 'post'])
@login_required
def edit(id):
    try:
        # Select contrat in BDD
        contrat = db.session.get(Contrat, id)
        appartement = db.session.get(Appartement, contrat.appartement_id)
        locataire = db.session.get(Locataire, contrat.locataire_id)

        if request.method == 'GET':
            form = ContratForm(obj=contrat)
        else:
            form = ContratForm()
        form.appartement_id.choices = [(appartement.id, appartement.libelle.upper() + ', ' + appartement.adresse)]
        form.appartement_id.render_kw = {'readonly': 'readonly'}
        form.locataire_id.choices = [(locataire.id, locataire.nom + ' ' + locataire.prenom)]
        form.locataire_id.render_kw = {'readonly': 'readonly'}
        if form.validate_on_submit():
            # Update contrat in BDD
            contrat.libelle = form.libelle.data
            contrat.date_debut = form.date_debut.data
            contrat.date_fin = form.date_fin.data
            db.session.commit()
            # Message flash ok
            flash('Le contrat a bien été modifié', 'success')
            return redirect(url_for('contrat_bp.index'))
        return render_template('contrat/add.html', form=form, title='Modifier un contrat', route='contrat_bp')
    except Exception:
        flash('Erreur, un problème est survenu lors de la modification du contrat', 'danger')
        return redirect(url_for('contrat_bp.index'))

@contrat_bp.route('/contrat/del/<int:id>', methods=['get', 'post'])
@login_required
def delete(id):
    try:
        # Select contrat in BDD
        contrat = db.session.get(Contrat, id)
        # Delete contrat in BDD
        db.session.delete(contrat)
        db.session.commit()
        # Message flash ok
        flash('Le contrat a bien été supprimé', 'success')
        return redirect(url_for('contrat_bp.index'))
    except Exception:
        flash('Erreur, un problème est survenu lors de la suppression du contrat', 'danger')
        return redirect(url_for('contrat_bp.index'))