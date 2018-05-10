# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
This code creates:

1) a SQLAlchemy Engine that will interact with
our dockerized PostgreSQL database

2) a SQLAlchemy ORM session factory bound to this engine,

3) and a base class for our classes definitions.

"""

db_url = 'localhost:5433'
db_name = 'ontology-db'
db_user = 'postgres'
db_password = 'ONTOLOGY-DB'
engine = create_engine('postgresql://%s:%s@%s/%s' % (db_user, db_password, db_url, db_name))

# Unit of Work pattern
Session = sessionmaker(bind=engine)

# AKA Data Base
Base = declarative_base()
