import os
from flask import Flask, Blueprint
from flask_security import Security, SQLAlchemyUserDatastore
from .db import db
from .security import flask_bcrypt
from .models import User, Role
from sqlalchemy import exc
from blueprints import init_app
from instance.config import DevelopmentConfig, ProductionConfig, TestingConfig

def create_app(config_name=DevelopmentConfig):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_name)
    # initialisation de la base de données
    db.init_app(app)
    # enregistrement des blueprints
    init_app(app)

    # Initialisation de bcrypt
    flask_bcrypt.init_app(app)
    # Configuration du Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    return app

