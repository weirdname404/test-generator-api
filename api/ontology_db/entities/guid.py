# coding=utf-8

from sqlalchemy import Column, String, Integer

from api.ontology_db.db_config.base import Base


# Attribute
class Guid(Base):
    __tablename__ = 'guids'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name
