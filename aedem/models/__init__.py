from flask import current_app

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('{dialect}://{user}:{pwd}@{host}:{port}/{dbname}'.format(
    dialect = current_app.config['DB_DIALECT'],
    user = current_app.config['DB_USERNAME'],
    pwd = current_app.config['DB_PASSWORD'],
    host = current_app.config['DB_HOST'],
    port = current_app.config['DB_PORT'],
    dbname = current_app.config['DB_NAME']
))

Session = scoped_session(sessionmaker())
Base = declarative_base()

def initialize_database(engine):
    Session.configure(bind = engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)