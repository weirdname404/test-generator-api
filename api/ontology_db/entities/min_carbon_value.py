# coding=utf-8

from sqlalchemy import Column, String, Integer

from .db_config.base import Base


# Attribute
class MinCarbonValue(Base):
    __tablename__ = 'min_carbon_values'

    id = Column(Integer, primary_key=True)
    value = Column(String(20))

    def __init__(self, value):
        self.value = value
