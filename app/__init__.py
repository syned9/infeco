import os
from flask import Flask, Blueprint
# from app import db
from .db import db
from sqlalchemy import exc
# from app.blueprints import init_app
from instance.config import DevelopmentConfig, ProductionConfig, TestingConfig

def create_app(config_name=DevelopmentConfig):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)

    # init_app(app)
    return app

