# coding=utf-8

import unittest

from api.ontology_db.db_config.base import Base, Session, engine
from api.ontology_db.entities.entity_class import EntityClass
from api.ontology_db.entities.scales import Scale
from api.ontology_db.entities.steel import Steel
from api.ontology_db.entities.guid import Guid, ScaleGuid, ClassGuid
from api.ontology_db.ontology_parser import MAX_OBJS, MAX_SCALES

# generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# parsing starts from the 2d row, not from the 1st
MAX_OBJS -= 1

ALL_SCALES = session.query(Scale).all()
ALL_OBJECTS = session.query(Steel).all()
SCALE_1 = ALL_SCALES[0]
SCALE_3 = ALL_SCALES[2]
OBJECT_1 = ALL_OBJECTS[0]
OBJECT_2 = ALL_OBJECTS[1]


def test_scales_data():
    assert len(ALL_SCALES) == MAX_SCALES
    assert SCALE_1.name == 'Способ раскисления'
    assert SCALE_1.values[0].value == 'Спокойная'
    assert SCALE_3.name == 'Содержание легирующих элементов'
    assert SCALE_3.values[0].value == 'Азот'
    assert SCALE_1.guid != SCALE_3.guid


def test_objects_data():
    assert len(ALL_OBJECTS) == MAX_OBJS
    assert OBJECT_1.name == 'Ст0'
    assert OBJECT_1.deoxidizing_type.name == 'Полуспокойная'
    assert OBJECT_2.name == 'Ст1кп'
    assert OBJECT_2.deoxidizing_type.name == 'Кипящая'
    assert OBJECT_2.quality.name == 'Обыкновенного качества'
    assert OBJECT_2.alloying_elements[0].name == 'Кремний'


def test_object_relations():
    assert OBJECT_1.entity_class == OBJECT_2.entity_class
    assert OBJECT_1.gost == OBJECT_2.gost
    assert OBJECT_1.guid != OBJECT_2.guid
    assert OBJECT_1.deoxidizing_type != OBJECT_2.deoxidizing_type
    assert OBJECT_1.quality == OBJECT_2.quality
    assert OBJECT_1.alloying_elements == OBJECT_2.alloying_elements
    assert OBJECT_1.max_carbon_value != OBJECT_2.max_carbon_value


def test_data_ambiguity():
    obj_1 = session.query(Steel).filter(Steel.name == "Ст3Гпс").all()[0]
    obj_2 = session.query(Steel).filter(Steel.name == "Ст5Гпс").all()[0]
    assert obj_1.max_carbon_value.value == '0.22'
    # the values are the same,
    # but the value objects are different, due to different scales
    assert obj_1.max_carbon_value.value == obj_2.min_carbon_value.value
    assert obj_1.max_carbon_value != obj_2.max_carbon_value
    # the same class and guid
    assert obj_1.entity_class == obj_2.entity_class
    assert obj_1.entity_class.guid == obj_2.entity_class.guid


def test_data_consistency():
    all_guids = session.query(Guid).all()
    all_scale_guids = session.query(ScaleGuid).all()
    all_class_guids = session.query(ClassGuid).all()
    all_classes = session.query(EntityClass).all()
    assert len(ALL_SCALES) == len(all_scale_guids)
    assert len(all_class_guids) == len(all_classes)
    assert len(ALL_OBJECTS) == len(all_guids)
