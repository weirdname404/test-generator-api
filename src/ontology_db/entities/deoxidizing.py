# coding=utf-8

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from .db_config.base import Base


# Attribute
class DeoxidizingType(Base):
    __tablename__ = 'deoxidizing_types'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    steels = relationship('Steel', back_populates='deoxidizing_type')

    def __init__(self, value):
        self.value = value
