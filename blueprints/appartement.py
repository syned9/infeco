from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash
from app.forms import AppartementForm
from app.models import Appartement
from app import db

appartement_bp = Blueprint('appartement_bp', __name__)

@appartement_bp.route('/appartement')
def index():
    # Select all appartements in BDD
    appartements = db.session.query(Appartement).all()
    # Trier les appartements par libelle
    appartements_tries = sorted(appartements, key=lambda x: x.libelle)
    return render_template('appartement/index.html', title='Liste appartements', appartements=appartements_tries, nb_appartements=len(appartements_tries))

@appartement_bp.route('/appartement/add', methods=['get', 'post'])
def add():
    try:
        form = AppartementForm()
        if form.validate_on_submit():
            # Insert appartement in BDD
            appartement = Appartement(libelle=form.libelle.data, adresse=form.adresse.data, complement=form.complement.data,
                                    ville=form.ville.data, code_postal=form.code_postal.data, loyer=form.loyer.data,
                                    charges=form.charges.data, depot_garantie=form.depot_garantie.data, agence_id=1)
            db.session.add(appartement)
            db.session.commit()
            # Message flash ok
            flash('L\'appartement a bien été enregistrer', 'success')
            return redirect(url_for('appartement_bp.index'))
        return render_template('appartement/add.html', form=form, title='Ajouter un appartement', route='appartement_bp')
    except Exception:
        flash('Erreur, un problème est survenu lors de l\'ajout de l\'appartement', 'danger')
        return redirect(url_for('appartement_bp.index'))

@appartement_bp.route('/appartement/edit/<int:id>', methods=['get', 'post'])
def edit(id):
    try:
        # Select appartement in BDD
        appartement = db.session.get(Appartement, id)
        if request.method == 'GET':
            form = AppartementForm(obj=appartement)
        else:
            form = AppartementForm()
        if form.validate_on_submit():
            # Update appartement in BDD
            appartement.libelle = form.libelle.data
            appartement.adresse = form.adresse.data
            appartement.complement = form.complement.data
            appartement.ville = form.ville.data
            appartement.code_postal = form.code_postal.data
            appartement.loyer = form.loyer.data
            appartement.charges = form.charges.data
            appartement.depot_garantie = form.depot_garantie.data
            db.session.commit()
            # Message flash ok
            flash('L\'appartement a bien été modifié', 'success')
            return redirect(url_for('appartement_bp.index'))
        return render_template('appartement/add.html', form=form, title='Modifier un appartement', route='appartement_bp')
    except Exception:
        flash('Erreur, un problème est survenu lors de la modification de l\'appartement', 'danger')
        return redirect(url_for('appartement_bp.index'))

@appartement_bp.route('/appartement/del/<int:id>', methods=['get', 'post'])
def delete(id):
    try:
        # Select appartement in BDD
        appartement = db.session.get(Appartement, id)
        # Delete appartement in BDD
        db.session.delete(appartement)
        db.session.commit()
        # Message flash ok
        flash('L\'appartement a bien été supprimé', 'success')
        return redirect(url_for('appartement_bp.index'))
    except Exception:
        flash('Erreur, un problème est survenu lors de la suppression de l\'appartement', 'danger')
        return redirect(url_for('appartement_bp.index'))