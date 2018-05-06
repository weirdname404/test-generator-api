# coding=utf-8

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from db_config.base import Base


class Entity_class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    steels = relationship('Steel', back_populates='entity_class')

    def __init__(self, value):
        self.value = value
