# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from .db_config.base import Base

# Object
steels_alloying_elements_association = Table(
    'steels_alloying_elements', Base.metadata,
    Column('steel_id', Integer, ForeignKey('steels.id')),
    Column('alloying_element_id', Integer, ForeignKey('alloying_elements.id'))
)


class Steel(Base):
    __tablename__ = 'steels'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gost_id = Column(Integer, ForeignKey('gosts.id'))
    deoxidizing_type_id = Column(Integer, ForeignKey('deoxidizing_types.id'))
    quality_id = Column(Integer, ForeignKey('quality_types.id'))
    min_carbon_value_id = Column(Integer, ForeignKey('min_carbon_values.id'))
    max_carbon_value_id = Column(Integer, ForeignKey('max_carbon_values.id'))
    entity_class_id = Column(Integer, ForeignKey('entity_classes.id'))

    guid = relationship('Guid', uselist=False, back_populates='steel')
    gost = relationship('Gost', back_populates='steels')
    deoxidizing_type = relationship('Deoxidizing_type', back_populates='steels')
    quality = relationship('Quality_type', back_populates='steels')
    alloying_elements = relationship('Alloying_element', secondary=steels_alloying_elements_association,
                                     backref='steels')
    min_carbon_value = relationship('Min_carbon_value', back_populates='steels')
    max_carbon_value = relationship('Max_carbon_value', back_populates='steels')
    entity_class = relationship('Entity_class', back_populates='steels')

    def __init__(self, guid, name, entity_class, gost, deoxidizing_type, quality, min_carbon_value, max_carbon_value):
        self.guid = guid
        self.name = name
        self.entity_class = entity_class
        self.gost = gost
        self.deoxidizing_type = deoxidizing_type
        self.quality = quality
        self.min_carbon_value = min_carbon_value
        self.max_carbon_value = max_carbon_value
