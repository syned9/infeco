from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from flask import current_app as flask_app

db = SQLAlchemy()
# Base = declarative_base()
# engine = create_engine(url=flask_app.config['SQLALCHEMY_DATABASE_URI'], echo=True, future=True)

# Session = sessionmaker(bind=engine)


# def init_db():
#     Base.metadata.create_all(bind=engine)