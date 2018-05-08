# coding=utf-8

from sqlalchemy import Column, String, Integer

from .db_config.base import Base


# Attribute
class DeoxidizingType(Base):
    __tablename__ = 'deoxidizing_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    def __init__(self, name):
        self.name = name
