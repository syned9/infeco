from flask import Blueprint, redirect, url_for, flash, send_file
from datetime import date
import datetime
import tempfile
from dateutil.relativedelta import relativedelta
from fpdf import FPDF
from app.models import Contrat, Quittance
from app import db
from sqlalchemy.orm import joinedload
from flask_security import login_required

quittance_bp = Blueprint('quittance_bp', __name__)

@quittance_bp.route('/quittance/add/<int:contrat_id>', methods=['get', 'post'])
@login_required
def add(contrat_id):
    try:
        date_actuelle = date.today()
        contrat = db.session.get(Contrat, contrat_id)
        # Charger les relations pour éviter les requêtes supplémentaires
        db.session.query(Contrat).options(joinedload(Contrat.paiements), joinedload(Contrat.appartement)).filter(Contrat.id == contrat_id)
        # Vérifie si le contrat est terminé ou pas 
        if date_actuelle > contrat.date_fin:
            delta = relativedelta(contrat.date_fin + datetime.timedelta(days=1), contrat.date_debut)
            date_fin = contrat.date_fin
        else:
            delta = relativedelta(date_actuelle + datetime.timedelta(days=1), contrat.date_debut)
            date_fin = date_actuelle
        # Ne fait pas de prorata, donc si un mois est commencé il doit être payé    
        if delta.days > 0:
            montantTotalDu = (contrat.appartement.loyer + contrat.appartement.charges) * (delta.months + 1) 
        else:
            montantTotalDu = (contrat.appartement.loyer + contrat.appartement.charges) * delta.months

        # Calcule des montants versés par le locataire 
        montantTotalVerse = 0
        montantTotalCharges = 0
        montantTotalLoyer = 0
        for paiement in contrat.paiements:
            if paiement.type_paiement_id == 1:
                montantTotalLoyer += paiement.montant
            elif paiement.type_paiement_id == 2:
                montantTotalCharges += paiement.montant
        
        montantTotalVerse = montantTotalCharges + montantTotalLoyer

        if (montantTotalDu <= montantTotalVerse):
            # Créer une instance de la classe MyPDF
            pdf = FPDF()

            # Ajouter une page
            pdf.add_page()

            # Écrire du texte dans le document
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'Quittance de loyer', 0, 1)
            pdf.set_font('Arial', '', 16)
            pdf.set_text_color(0,0,255)
            pdf.cell(0, 10, 'Adresse de location : ', 0, 1)
            pdf.set_font('Arial', '', 12)
            pdf.set_text_color(0,0,0)
            pdf.cell(0, 10, 'Adresse: ' + contrat.appartement.adresse, 0, 1)
            pdf.cell(0, 10, 'Code postal: ' + contrat.appartement.code_postal, 0, 1)
            pdf.cell(0, 10, 'ville: ' + contrat.appartement.ville, 0, 1)
            pdf.set_font('Arial', '', 16)
            pdf.set_text_color(0,0,255)
            pdf.cell(0, 10, 'Détail du réglement : ', 0, 1)
            pdf.set_font('Arial', '', 12)
            pdf.set_text_color(0,0,0)
            pdf.cell(0, 10, 'Loyer: ' + str(montantTotalLoyer) + ' euros', 0, 1)
            pdf.cell(0, 10, 'Provision des charges: ' + str(montantTotalCharges) + ' euros', 0, 1)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Total: ' + str(montantTotalVerse) + ' euros', 0, 1)
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, 'Fait le : ' + date_actuelle.strftime("%d/%m/%Y"), 0, 1)


            filename = 'Quittance_'+ date_actuelle.strftime("%d/%m/%Y") +'.pdf'
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                # Enregistrer le PDF dans le fichier temporaire
                pdf.output(temp_file.name)

                # Récupérer le chemin complet du fichier temporaire
                temp_file_path = temp_file.name

            # Insert quittance in BDD
            quittance = Quittance(date_debut=contrat.date_debut, date_fin=date_fin,
                                    montant=montantTotalVerse, date_creation=date_actuelle, locataire_id=contrat.locataire_id)
            db.session.add(quittance)
            db.session.commit()

            # Envoyer le fichier en tant que réponse de téléchargement
            return send_file(temp_file_path, as_attachment=True, download_name=filename)

        flash('Impossible de générer la Quittance car le locataire n\'est pas à jour dans ses loyer', 'warning')
        return redirect(url_for('locataire_bp.details', id=contrat.locataire_id))
    except Exception:
        flash('Erreur, un problème est survenu lors de l\'ajout d\'une quittance', 'danger')
        return redirect(url_for('locataire_bp.details', id=contrat.locataire_id))

@quittance_bp.route('/quittance/del/<int:id>', methods=['get', 'post'])
@login_required
def delete(id):
    try:
        # Select quittance in BDD
        quittance = db.session.get(Quittance, id)
        locataire_id = quittance.locataire_id
        # Delete quittance in BDD
        db.session.delete(quittance)
        db.session.commit()

        flash('La Quittance a bien été suprimée', 'success')
        return redirect(url_for('locataire_bp.details', id=locataire_id))
    except Exception:
        flash('Erreur, un problème est survenu lors de la suppression de la quittance', 'danger')
        return redirect(url_for('locataire_bp.details', id=locataire_id))