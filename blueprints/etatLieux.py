from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.forms import EtatLieuxForm
from app.models import EtatLieux, Contrat
from app import db
from sqlalchemy.orm import joinedload
from flask_security import login_required

etatLieux_bp = Blueprint('etatLieux_bp', __name__)

@etatLieux_bp.route('/etatLieux')
@login_required
def index():
     # Select all etatLieuxs in BDD
    etatLieux = db.session.query(EtatLieux).all()
    for etatLieu in etatLieux:
        # Charger les relations pour éviter les requêtes supplémentaires
        db.session.query(EtatLieux).options(joinedload(EtatLieux.contrat)).filter(EtatLieux.id == etatLieu.id)
    # Trier les etatLieuxs par date
    etatLieux_tries = sorted(etatLieux, key=lambda x: x.date)
    return render_template('etatLieux/index.html', title='Liste état des lieux', allEtatLieux=etatLieux_tries, nb_etatLieux=len(etatLieux_tries))

@etatLieux_bp.route('/etatLieux/add', methods=['get', 'post'])
@login_required
def add():
    try:
        contrats = db.session.query(Contrat).all()
        # Trier les contrats par libelle
        contrats_tries = sorted(contrats, key=lambda x: x.libelle)
        form = EtatLieuxForm()
        form.contrat_id.choices = [(contrat.id, contrat.libelle) for contrat in contrats_tries]
        if form.validate_on_submit():
            # Insert etatLieux in BDD
            etatLieux = EtatLieux(date=form.date.data, remarque=form.remarque.data,
                                    situation=int(form.situation.data), contrat_id=form.contrat_id.data)
            db.session.add(etatLieux)
            db.session.commit()
            # Message flash ok
            flash('L\'état des lieux a bien été enregistrer', 'success')
            return redirect(url_for('etatLieux_bp.index'))
        return render_template('etatLieux/add.html', form=form, title='Ajouter un état des lieux', route='etatLieux_bp')
    except Exception:
        flash('Erreur, un problème est survenu lors de l\'ajout d\'un état des lieux', 'danger')
        return redirect(url_for('etatLieux_bp.index'))

@etatLieux_bp.route('/etatLieux/edit/<int:id>', methods=['get', 'post'])
@login_required
def edit(id):
    try:
        # Select etatLieux in BDD
        etatLieux = db.session.get(EtatLieux, id)
        # contrat = db.session.get(Contrat, etatLieux.contrat_id)
        contrats = db.session.query(Contrat).all()
        # Trier les contrats par libelle
        contrats_tries = sorted(contrats, key=lambda x: x.libelle)
        if request.method == 'GET':
            if etatLieux.situation:
                etatLieux.situation = 1
            else:
                etatLieux.situation = 0
            form = EtatLieuxForm(obj=etatLieux)
        else:
            form = EtatLieuxForm()
        form.contrat_id.choices = [(contrat.id, contrat.libelle) for contrat in contrats_tries]
        if form.validate_on_submit():
            # Update etatLieux in BDD
            etatLieux.date = form.date.data
            etatLieux.remarque = form.remarque.data
            etatLieux.situation = int(form.situation.data)
            etatLieux.contrat_id = form.contrat_id.data
            db.session.commit()
            # Message flash ok
            flash('L\'état des lieux a bien été modifié', 'success')
            return redirect(url_for('etatLieux_bp.index'))
        
        return render_template('etatLieux/add.html', form=form, title='Modifier un état des lieux', route='etatLieux_bp')
    except Exception:
        flash('Erreur, un problème est survenu lors de la modification de l\'état des lieux', 'danger')
        return redirect(url_for('etatLieux_bp.index'))

@etatLieux_bp.route('/etatLieux/del/<int:id>', methods=['get', 'post'])
@login_required
def delete(id):
    try:
        # Select etatLieux in BDD
        etatLieux = db.session.get(EtatLieux, id)
        # Delete etatLieux in BDD
        db.session.delete(etatLieux)
        db.session.commit()
        # Message flash ok
        flash('L\'état des lieux a bien été supprimé', 'success')
        return redirect(url_for('etatLieux_bp.index'))
    except Exception:
        flash('Erreur, un problème est survenu lors de la suppression de l\'état des lieux', 'danger')
        return redirect(url_for('etatLieux_bp.index'))