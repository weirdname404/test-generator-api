# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from api.ontology_db.db_config.base import Base


# Steel guid
class Guid(Base):
    __tablename__ = 'guids'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


# Scale guid
class ScaleGuid(Base):
    __tablename__ = 'scale_guids'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    scale_id = Column(Integer, ForeignKey('scales.id'))
    scale = relationship('Scale', uselist=False, back_populates='guid')

    def __init__(self, name):
        self.name = name


# Entity class guid
class ClassGuid(Base):
    __tablename__ = 'class_guids'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    entity_class_id = Column(Integer, ForeignKey('entity_classes.id'))
    entity_class = relationship('EntityClass', uselist=False, back_populates='guid')

    def __init__(self, name):
        self.name = name
