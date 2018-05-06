# coding=utf-8

from sqlalchemy import Column, String, Integer
from db_config.base import Base


# Attribute
class Alloying_element(Base):
    __tablename__ = 'alloying_elements'

    id = Column(Integer, primary_key=True)
    value = Column(String)

    def __init__(self, value):
        self.value = value
