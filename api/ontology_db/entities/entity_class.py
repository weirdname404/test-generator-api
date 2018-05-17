# coding=utf-8

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from api.ontology_db.db_config.base import Base


class EntityClass(Base):
    __tablename__ = 'entity_classes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    guid = relationship('ClassGuid', uselist=False, back_populates='entity_class')

    def __init__(self, name, guid):
        self.name = name
        self.guid = guid
