# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from api.ontology_db.db_config.base import Base


class Scale(Base):
    __tablename__ = 'scales'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class ScaleValue(Base):
    __tablename__ = 'scale_values'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    scale_id = Column(Integer, ForeignKey('scales.id'))
    scale = relationship('Scale', backref='values')

    def __init__(self, value, scale):
        self.value = value
        self.scale = scale
