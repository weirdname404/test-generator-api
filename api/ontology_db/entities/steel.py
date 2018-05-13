# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from api.ontology_db.db_config.base import Base

# Object
steels_alloying_elements_association = Table(
    'steels_alloying_elements', Base.metadata,
    Column('steel_id', Integer, ForeignKey('steels.id')),
    Column('alloying_element_id', Integer, ForeignKey('alloying_elements.id'))
)


class Steel(Base):
    __tablename__ = 'steels'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    guid_id = Column(Integer, ForeignKey('guids.id'))
    entity_class_id = Column(Integer, ForeignKey('entity_classes.id'))
    gost_id = Column(Integer, ForeignKey('gosts.id'))
    deoxidizing_type_id = Column(Integer, ForeignKey('deoxidizing_types.id'))
    quality_id = Column(Integer, ForeignKey('quality_types.id'))
    min_carbon_value_id = Column(Integer, ForeignKey('min_carbon_values.id'))
    max_carbon_value_id = Column(Integer, ForeignKey('max_carbon_values.id'))

    guid = relationship('Guid', uselist=False, backref='steel')
    gost = relationship('Gost', backref='steels')
    deoxidizing_type = relationship('DeoxidizingType', backref='steels')
    quality = relationship('QualityType', backref='steels')
    alloying_elements = relationship('AlloyingElement', secondary=steels_alloying_elements_association,
                                     backref='steels')
    min_carbon_value = relationship('MinCarbonValue', backref='steels')
    max_carbon_value = relationship('MaxCarbonValue', backref='steels')
    entity_class = relationship('EntityClass', backref='steels')

    def __init__(self, name, guid):
        self.name = name
        self.guid = guid
