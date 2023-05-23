import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'developpement POC infeco'
    TEMPLATE_FOLDER = 'templates'
    SECURITY_PASSWORD_SALT = 'infecoblock3'

class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = os.environ['JAWSDB_URL']
    DEBUG = False
    FLASK_ENV = 'production'

class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://infeco:kyzSR9aj6ZGHVm@127.0.0.1:3306/infeco'

class TestingConfig(Config):
    TESTING = True
