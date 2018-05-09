# coding=utf-8

from sqlalchemy import Column, String, Integer

from .db_config.base import Base


# Attribute
class Gost(Base):
    __tablename__ = 'gosts'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    def __init__(self, name):
        self.name = name
