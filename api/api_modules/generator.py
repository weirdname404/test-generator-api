# coding=utf-8
import random
import uuid

from api.ontology_db.db_config.base import Base, Session, engine
from api.ontology_db.entities.scales import Scale
from api.ontology_db.entities.steel import Steel

Base.metadata.create_all(engine)
session = Session()


class OAConfig:
    q_type = Steel
    a_form = ''
    obj = Steel
    attr = Scale
    key = []
    positive = True
    answer_option = ''

    def __init__(self, q_type, a_form, ent1, ent2):
        self.q_type = q_type
        self.a_form = a_form
        self.obj = ent1
        self.attr = ent2


def generate_test(test_requirements):
    # connect to DB
    Base.metadata.create_all(engine)
    session = Session()

    all_tests = []

    for i in range(test_requirements.amount):
        test = {'guid': str(uuid.uuid4()).upper()}
        question_type = random.choice(test_requirements.request_question_types)
        answer_form = random.choice(test_requirements.request_answer_forms)
        test['question_type'] = question_type
        test['answer_form'] = answer_form

        entity_1 = random.choice(test_requirements.request_entities1)
        entity_2 = random.choice(test_requirements.request_entities2)

        # if the answer form is binary, we need to randomly choose if the answer is positive or negative
        positive = bool(random.getrandbits(1))

        stem, distractors, key = '', [], []

        if question_type == 'O>A':
            steel_object, attribute = define_object_attribute(entity_1, entity_2)
            # generator func takes lots of args, that's why special config class was created
            config = OAConfig(question_type, answer_form, steel_object, attribute)
            config.positive = positive
            test['entity1'] = config.obj.guid.name if config.q_type == 'O>A' else config.attr.guid.name
            test['entity2'] = config.attr.guid.name if config.q_type == 'O>A' else config.obj.guid.name
            config.key = generate_key(config.attr.name, config.obj)
            stem, distractors, key = generate_object_attribute_question(config)

        # TODO other question types

        test['stem'] = stem
        test['distractors'] = distractors
        test['key'] = key
        all_tests.append(test)

    session.close()

    return all_tests


def define_object_attribute(steel_object, attribute):
    steel_object = session.query(Steel).filter(Steel.name == steel_object).all()
    attribute = session.query(Scale).filter(Scale.name == attribute).all()

    return steel_object[0], attribute[0]


# defining [correct attribute value] for an object
def generate_key(attribute, steel_object):
    if 'в процентах' in attribute:
        attribute = attribute.split()[2]

    relations_dict = {
        'Способ раскисления': [steel_object.deoxidizing_type.name],
        'Содержание легирующих элементов': [i.name for i in steel_object.alloying_elements],
        'Характеристика качества': [steel_object.quality.name],
        'ГОСТ сплава': [steel_object.gost.name],
        'углерода': [steel_object.min_carbon_value.value + '-' + steel_object.max_carbon_value.value],
        'марганца': []
    }

    return relations_dict[attribute]


# combine min and max values of the element to create 'v1-v2' distractors
def generate_min_max_distractors(distractors, attribute):
    attribute = attribute.name.split()[2]
    min_max_distractors = {
        'углерода': [steel.min_carbon_value.value + "-" + steel.max_carbon_value.value for steel in distractors]
    }
    return min_max_distractors[attribute]


# generating a stem
# key is checked for YES/NO questions to understand will it be used in stem or not
def generate_object_attribute_question(config):
    steel_object, attribute, key, q_type, a_form = config.obj, config.attr, config.key, config.q_type, config.a_form
    # distractors will be either list of scale values or list of scale values and list of steel objs
    distractors = generate_distractors(steel_object, attribute, key)

    if a_form == 'binary':
        key, config.answer_option = define_answer_and_distractor(config, distractors)
        distractors = ['Да', 'Нет']
        stem = generate_oa_stem(config)

    else:
        distractors = key + distractors
        stem = generate_oa_stem(config)

    return stem, distractors, key


def generate_oa_stem(config):
    steel_object, attribute, q_type, answer_option = config.obj, config.attr, config.q_type, config.answer_option
    binary = True if config.a_form == 'binary' else False
    stem = ''
    if q_type == 'O>A':
        if binary:
            if attribute.name == 'Способ раскисления':
                stem += "Верно ли, что сталь %s по способу раскисления %s?" % (steel_object.name, answer_option)

            elif attribute.name == 'Содержание легирующих элементов':
                stem += "Содержит ли сталь %s %s в качестве легирующего элемента?" % (steel_object.name, answer_option)

            elif attribute.name == 'Характеристика качества':
                stem += "Верно ли, что сталь %s %s?" % (steel_object.name, answer_option)

            elif attribute.name == 'ГОСТ сплава':
                stem += "Входит ли сталь %s в %s?" % (steel_object.name, answer_option.upper())

            else:
                stem += "Верно ли, что массовая доля %s в процентах у стали %s - %s?" % (
                    attribute.name.split()[2], steel_object.name, answer_option)

        # Option(s)
        else:
            if attribute.name == 'Способ раскисления':
                stem += "Охарактеризуйте с точки зрения способа раскисления сталь %s:" % steel_object.name

            elif attribute.name == 'Содержание легирующих элементов':
                stem += "Определите какие легирующие элементы входят в состав стали %s:" % steel_object.name

            elif attribute.name == 'Характеристика качества':
                stem += "Сталь %s можно охарактеризовать с точки зрения качества как:" % steel_object.name

            elif attribute.name == 'ГОСТ сплава':
                stem += "Укажите к какому ГОСТу относится сталь %s:" % steel_object.name

            else:
                stem += "Определите массовую долю %s в процентах у стали %s:" % (
                    attribute.name.split()[2], steel_object.name)
    # 'A>O'
    else:
        if binary:
            pass

        # Option(s)
        else:
            pass

    return stem


# Getting all values from chosen Scale and deleting one or several correct answers
# Optional - fetching also all steel objects
def generate_distractors(steel_object, attribute, key):
    # The key is removed from distractors anyway, btw it will be added later.
    # This is done to avoid random choice uncertainty.
    distractors = session.query(Steel).filter(
        Steel.name != steel_object.name).all() if 'в процентах' in attribute.name \
        else list({i.value for i in attribute.values} - set(key))

    random.shuffle(distractors)
    distractors = distractors[:4]

    return generate_min_max_distractors(distractors, attribute) if 'в процентах' in attribute.name \
        else distractors

    # TODO
    # This part is invalid, because objects should be filtered by SCALE NAME and SCALE VALUE
    # # object distractors are optional
    # if q_type == 'A>O':
    #     objects_distractors = session.query(Steel).filter(Steel.name != object.name).all()
    #     random.shuffle(objects_distractors)
    #     objects_distractors = [i.name for i in objects_distractors[:4]]
    #
    # return scale_distractors, objects_distractors


# key is a list [], we can handle single and multiple answers
def define_answer_and_distractor(config, distractors):
    if config.positive:
        # the answer is positive, we do not need a distractor
        # answers may be several
        answer_option = config.key[random.randint(0, len(config.key) - 1)]
        key = ['Да']
    else:
        answer_option = random.choice(distractors)
        key = ['Нет']

    return key, answer_option.lower()
