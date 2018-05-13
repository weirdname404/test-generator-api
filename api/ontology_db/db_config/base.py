# coding=utf-8

import os
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

try:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    
except KeyError:
    SQLALCHEMY_DATABASE_URI = ''

# Local setup
db_url = 'localhost:5432'
db_name = 'ontology-db'
db_user = 'postgres'
db_password = 'ONTOLOGY-DB'

LOCAL_URI = 'postgresql://%s:%s@%s/%s' % (db_user, db_password, db_url, db_name)

SQLALCHEMY_DATABASE_URI = LOCAL_URI if len(LOCAL_URI) >= len(SQLALCHEMY_DATABASE_URI) else SQLALCHEMY_DATABASE_URI

# engine = create_engine()
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Unit of Work pattern
Session = sessionmaker(bind=engine)

# AKA Data Base
Base = declarative_base()
