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

        stem, distractors, key = '', [], []

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
    if 'в процентах' in attribute:
        attribute = attribute.split()[2]

    relations_dict = {
        'Способ раскисления': [object.deoxidizing_type.name],
        'Содержание легирующих элементов': [i.name for i in object.alloying_elements],
        'Характеристика качества': [object.quality.name],
        'ГОСТ сплава': [object.gost.name],
        'углерода': [object.min_carbon_value.value + '-' + object.max_carbon_value.value],
        'марганца': []
    }

    return relations_dict[attribute]


# combine min and max values of the element to create 'v1-v2' distractors
def generate_min_max_distractors(attribute):
    scale = session.query(Scale).filter(Scale.name == attribute.name).all()[0]
    value_num = len(scale.values)
    print(value_num)
    attribute = attribute.name.split()[2]

    min_max_distractors = {'углерода':
                               [session.query(ScaleValue).join(Scale).filter(
                                   Scale.name == 'Максимальная доля углерода в процентах').all()[i].value +
                                '-' + session.query(ScaleValue).join(Scale).filter(
                                   Scale.name == 'Минимальная доля углерода в процентах').all()[i].value
                                for i in range(value_num)]
                           } # TODO fix the bug len(min) != len(max) <- !!!!!

    return set(min_max_distractors[attribute])


# generating stem
# key is checked for YES/NO questions to understand will it be used in stem or not
def generate_object_attribute_question(object, attribute, answer_form, key, positive):
    stem = ""
    distractors = generate_distractors(attribute, key)

    if answer_form == 'binary':
        key, answer_option = define_answer_and_distractor(key, positive, distractors)
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

    else:
        options = []

        for _ in range(4):
            rand_choice = random.choice(distractors)
            options.append(rand_choice)
            distractors.remove(rand_choice)

        distractors = key + options

        if attribute.name == 'Способ раскисления':
            stem += "Охарактеризуйте с точки зрения способа раскисления сталь %s:" % (object.name)

        elif attribute.name == 'Содержание легирующих элементов':
            stem += "Определите какие легирующие элементы входят в состав стали %s:" % (object.name)

        elif attribute.name == 'Характеристика качества':
            stem += "Сталь %s можно охарактеризовать с точки зрения качества как:" % (object.name)

        elif attribute.name == 'ГОСТ сплава':
            stem += "Укажите к какому ГОСТу относится сталь %s:" % (object.name)

        else:
            stem += "Определите массовую долю %s в процентах у стали %s:" % (attribute.name.split()[2], object.name)

    return stem, distractors, key


# Get all values from chosen Scale and delete a correct answer or answers from there
def generate_distractors(attribute, key):
    distractors = generate_min_max_distractors(attribute) \
        if 'в процентах' in attribute.name else {i.value for i in attribute.values}
    # eliminating 2 sets intersection
    return list(distractors - set(key))


# key is a list [], we can handle single and multiple answers
def define_answer_and_distractor(key, positive, distractors):
    if positive:
        # the answer is positive, we do not need a distractors
        # answers may be several
        answer_option = key[random.randint(0, len(key) - 1)]
        key = ['Да']
    else:
        answer_option = random.choice(distractors)
        key = ['Нет']

    return key, answer_option.lower()
