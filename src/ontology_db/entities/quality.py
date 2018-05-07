# coding=utf-8

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from .db_config.base import Base


# Attribute
class QualityType(Base):
    __tablename__ = 'quality_types'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    steels = relationship('Steel', back_populates='quality')

    def __init__(self, value):
        self.value = value
