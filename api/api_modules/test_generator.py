# coding=utf-8
import random
import uuid

from api.ontology_db.db_config.base import Base, Session, engine
from api.ontology_db.entities.entity_class import EntityClass
from api.ontology_db.entities.scales import Scale, ScaleValue
from api.ontology_db.entities.steel import Steel

Base.metadata.create_all(engine)
session = Session()


def generate_test(n, request_question_types, request_answer_forms, request_entities1, request_entities2):
    # connect to DB
    Base.metadata.create_all(engine)
    session = Session()

    all_tests = []

    for i in range(n):
        test = {'guid': str(uuid.uuid4()).upper()}
        question_type = random.choice(request_question_types)
        answer_form = random.choice(request_answer_forms)
        test['question_type'] = question_type
        test['answer_form'] = answer_form

        entity_1 = random.choice(request_entities1)
        entity_2 = random.choice(request_entities2)

        # if the answer form is binary, we need to randomly choose if the answer is positive or negative
        positive = bool(random.getrandbits(1))

        if question_type == 'O>A' or 'A>O':
            object, attribute = define_object_attribute(entity_1, entity_2)
            test['entity1'] = object.guid.name if question_type == 'O>A' else attribute.guid.name
            test['entity2'] = attribute.guid.name if question_type == 'O>A' else object.guid.name
            key = generate_key(attribute.name, object)
            stem, distractors, key = generate_object_attribute_question(object, attribute, answer_form, key, positive)

        # TODO other question types

        test['stem'] = stem
        test['distractors'] = distractors
        test['key'] = key
        all_tests.append(test)

    session.close()

    return all_tests


def define_object_attribute(object, attribute):
    object = session.query(Steel).filter(Steel.name == object).all()
    attribute = session.query(Scale).filter(Scale.name == attribute).all()

    return object[0], attribute[0]


# defining [right answer]
def generate_key(attribute, object):
    relations_dict = {
        'Способ раскисления': [object.deoxidizing_type.name],
        'Максимальная доля углерода в процентах':
            [object.min_carbon_value.value + '-' + object.max_carbon_value.value],
        'Содержание легирующих элементов': [i.name for i in object.alloying_elements],
        'Характеристика качества': [object.quality.name],
        'ГОСТ сплава': [object.gost.name],
        'Минимальная доля марганца в процентах': [],
        'Максимальная доля марганца в процентах': [],
        'Минимальная доля углерода в процентах':
            [object.min_carbon_value.value + '-' + object.max_carbon_value.value]
    }

    return relations_dict[attribute]


# generating stem
# key is checked for YES/NO questions to understand will it be used in stem or not
def generate_object_attribute_question(object, attribute, answer_form, key, positive):
    stem = ""
    distractors = generate_distractors(attribute)

    if answer_form == 'binary':
        key, answer_option = define_answer_and_distractor(key, positive, distractors, attribute)
        distractors = ['Да', 'Нет']

        if attribute.name == 'Способ раскисления':
            stem += "Верно ли, что сталь %s по способу раскисления %s?" % (object.name, answer_option)

        elif attribute.name == 'Содержание легирующих элементов':
            stem += "Содержит ли сталь %s %s в качестве легирующего элемента?" % (object.name, answer_option)

        elif attribute.name == 'Характеристика качества':
            stem += "Верно ли, что сталь %s %s?" % (object.name, answer_option)

        elif attribute.name == 'ГОСТ сплава':
            stem += "Входит ли сталь %s в %s?" % (object.name, answer_option.upper())

        else:
            stem += "Верно ли, что %s у стали %s - %s?" % (attribute.name.lower(), object.name, answer_option)


    elif answer_form == 'choice':
        # TODO
        pass

    elif answer_form == 'options':
        # TODO
        pass

    return stem, distractors, key


def generate_distractors(attribute):
    if 'в процентах' in attribute.name:
        # TODO лепка значений для дистракторов
        pass

    return [value.value for value in attribute.values]


# key is a list [], we can handle single and multiple answers
def define_answer_and_distractor(key, positive, distractors, attribute):
    if positive:
        # the answer is positive, we do not need a distractors
        answer_option = key[random.randint(0, len(key) - 1)]
        key = ['Да']
    else:
        # the answer is negative, we create distractors by eliminating 2 sets intersection
        distractors = list(set(distractors) - set(key))
        answer_option = distractors[random.randint(0, len(distractors) - 1)]
        key = ['Нет']

    return key, answer_option.lower()
