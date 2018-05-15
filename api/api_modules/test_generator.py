# coding=utf-8
import random
import uuid

from api.ontology_db.db_config.base import Base, Session, engine
from api.ontology_db.entities.entity_class import EntityClass
from api.ontology_db.entities.scales import Scale
from api.ontology_db.entities.steel import Steel

Base.metadata.create_all(engine)
session = Session()


def generate_test(n, question_type, answer_form, entity_1, entity_2):
    Base.metadata.create_all(engine)
    session = Session()

    tests = []

    for i in range(len(n)):
        test = {"guid": str(uuid.uuid4()).upper()}
        question_type = random.choice(question_type)
        answer_form = random.choice(answer_form)
        test["question_type"] = question_type
        test["answer_form"] = answer_form

        entity_1 = random.choice(entity_1)
        entity_2 = random.choice(entity_2)

        # TODO

    session.close()

    return tests
