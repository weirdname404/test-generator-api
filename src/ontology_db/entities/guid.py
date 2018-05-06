# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db_config.base import Base


# Attribute
class Guid(Base):
    __tablename__ = 'guids'

    id = Column(Integer, primary_key=True)
    guid = Column(String)
    steel_id = Column(Integer, ForeignKey('steels.id'))
    steel = relationship('Steel', back_populates='guid')

    def __init__(self, guid, steel):
        self.guid = guid
        self.steel = steel
