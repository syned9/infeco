from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash
from app.forms import LocataireForm
from app.models import Locataire
from app import db

locataire_bp = Blueprint('locataire_bp', __name__)

@locataire_bp.route('/locataire')
def index():
    # Select all locataires in BDD
    locataires = db.session.query(Locataire).all()
    # Trier les locataires par nom
    locataires_tries = sorted(locataires, key=lambda x: x.nom)
    return render_template('locataire/index.html', title='Liste locataires', locataires=locataires_tries, nb_locataires=len(locataires_tries))

@locataire_bp.route('/locataire/add', methods=['get', 'post'])
def add():
    try:
        form = LocataireForm()
        if form.validate_on_submit():
            # Insert locataire in BDD
            locataire = Locataire(nom=form.nom.data, prenom=form.prenom.data,
                                    telephone=form.telephone.data, email=form.email.data)
            db.session.add(locataire)
            db.session.commit()
            # Message flash ok
            flash('Le locataire a bien été enregistrer', 'success')
            return redirect(url_for('locataire_bp.index'))
        return render_template('locataire/add.html', form=form, title='Ajouter un locataire', route='locataire_bp')
    except Exception:
        flash('Erreur, un problème est survenu lors de l\'ajout d\'un locataire', 'danger')
        return redirect(url_for('locataire_bp.index'))

@locataire_bp.route('/locataire/edit/<int:id>', methods=['get', 'post'])
def edit(id):
    try:
        # Select locataire in BDD
        locataire = db.session.get(Locataire, id)
        if request.method == 'GET':
            form = LocataireForm(obj=locataire)
        else:
            form = LocataireForm()
        if form.validate_on_submit():
            # Update locataire in BDD
            locataire.nom = form.nom.data
            locataire.prenom = form.prenom.data
            locataire.telephone = form.telephone.data
            locataire.email = form.email.data
            db.session.commit()
            # Message flash ok
            flash('Le locataire a bien été modifié', 'success')
            return redirect(url_for('locataire_bp.index'))
        return render_template('locataire/add.html', form=form, title='Modifier un locataire', route='locataire_bp')
    except Exception:
        flash('Erreur, un problème est survenu lors de la modification du locataire', 'danger')
        return redirect(url_for('locataire_bp.index'))

@locataire_bp.route('/locataire/del/<int:id>', methods=['get', 'post'])
def delete(id):
    try:
        # Select locataire in BDD
        locataire = db.session.get(Locataire, id)
        # Delete locataire in BDD
        db.session.delete(locataire)
        db.session.commit()
        # Message flash ok
        flash('Le locataire a bien été supprimé', 'success')
        return redirect(url_for('locataire_bp.index'))
    except Exception:
        flash('Erreur, un problème est survenu lors de la suppression du locataire', 'danger')
        return redirect(url_for('locataire_bp.index'))
