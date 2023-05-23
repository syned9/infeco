from .appartement import appartement_bp
from .locataire import locataire_bp
from .etatLieux import etatLieux_bp
from .paiement import paiement_bp
from .contrat import contrat_bp
from .quittance import quittance_bp
from .user import user_bp

def register_blueprints(app):
    app.register_blueprint(appartement_bp)
    app.register_blueprint(locataire_bp)
    app.register_blueprint(etatLieux_bp)
    app.register_blueprint(paiement_bp)
    app.register_blueprint(contrat_bp)
    app.register_blueprint(quittance_bp)
    app.register_blueprint(user_bp)

# appelé par l'application Flask lors de l'initialisation
def init_app(app):
    register_blueprints(app)