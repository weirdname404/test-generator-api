# coding=utf-8

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from base import Base


# Attribute
class Max_carbon_value(Base):
    __tablename__ = 'max_carbon_values'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    steels = relationship('Steel', back_populates='max_carbon_value')

    def __init__(self, value):
        self.value = value
