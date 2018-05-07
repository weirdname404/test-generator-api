# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db_config.base import Base


# Attribute
class Scale(Base):
    __tablename__ = 'scales'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    values = relationship('Scale_value', back_populates='scale')

    def __init__(self, name):
        self.name = name


class Scale_value(Base):
    __tablename__ = 'scale_values'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    scale_id = Column(Integer, ForeignKey('scales.id'))
    scale = relationship('Scale', back_populates='values')

    def __init__(self, value, scale):
        self.value = value
        self.scale = scale