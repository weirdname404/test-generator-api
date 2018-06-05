# coding=utf-8
import random
import uuid
import time

from api.ontology_db.db_config.base import Base, Session, engine
from api.ontology_db.entities.scales import Scale
from api.ontology_db.entities.steel import Steel
from api.api_modules.generator_modules.stem_generator import generate_stem
from api.api_modules.generator_modules.generation_config import Config

# connect to DB
Base.metadata.create_all(engine)
session = Session()

# constants
ALL_STEELS = session.query(Steel).all()

SA_OBJ = 'steel_attr_obj'
SA_CLASS = 'steel_attr_class'
KEY = 'key'


# main generator func
def generate_test(test_requirements):
    start_time = time.time()
    all_tests = []
    # let's check do we support requested question type or not
    for i in test_requirements.request_question_types:
        if i not in ['O>A', 'O>A>O', 'A>O', "A>O>A"]:
            i += ' question type is not supported'
            all_tests.append(i)
            return all_tests

    for _ in range(test_requirements.amount):
        question_type, answer_form, entity_1, entity_2 = make_random_choice(test_requirements)
        config = Config(question_type, answer_form)
        config.obj, config.attr = define_object_attribute(entity_1, entity_2)

        # if the answer form is binary, we need to randomly choose will the answer to the Q. be positive or negative
        config.positive = bool(random.getrandbits(1))

        # generate a JSON response form for a single test
        test = generate_json(config)
        test['stem'], test['distractors'], test['key'] = generate_test_item(config)

        all_tests.append(test)

    print(f"--- {time.time() - start_time} seconds ---")

    return all_tests


# randomly choose params from the request
def make_random_choice(test_requirements):
    inputs_list = [test_requirements.request_question_types, test_requirements.request_answer_forms,
                   test_requirements.request_entities1, test_requirements.request_entities2]

    return map(random.choice, inputs_list)


# define the Steel and Scale objects
def define_object_attribute(steel_object, attribute):
    steel_object = session.query(Steel).filter(Steel.name == steel_object).first()
    attribute = session.query(Scale).filter(Scale.name == attribute).first()

    return steel_object, attribute


# define a response-JSON variables
def generate_json(config):
    test = {'guid': str(uuid.uuid4()).upper(), 'question_type': config.q_type, 'answer_form': config.a_form,
            'entity1': config.obj.guid.name
            if config.q_type == 'O>A' or config.q_type == 'O>A>O' else config.attr.guid.name,
            'entity2': config.attr.guid.name
            if config.q_type == 'O>A' or config.q_type == 'O>A>O' else config.obj.guid.name}

    return test


# attribute value, attribute class, steel.attribute object definition
def define(request_code, steel_object, attribute_name):
    if 'в процентах' in attribute_name:
        attribute_name = attribute_name.split()[2]

    # Classes and Objects
    # {attribute_name: [attributeClass, Steel.attribute, [steel_obj.attribute.value]}
    attribute_dict = {
        'Способ раскисления': [steel_object.deoxidizing_type,
                               Steel.deoxidizing_type, [steel_object.deoxidizing_type.name]],

        'Содержание легирующих элементов': [steel_object.alloying_elements, Steel.alloying_elements,
                                            [i.name for i in steel_object.alloying_elements]],

        'Характеристика качества': [steel_object.quality, Steel.quality, [steel_object.quality.name]],
        'ГОСТ сплава': [steel_object.gost, Steel.gost, [steel_object.gost.name]],

        'углерода': [[steel_object.min_carbon_value, steel_object.max_carbon_value],
                     [Steel.min_carbon_value, Steel.max_carbon_value],
                     [steel_object.min_carbon_value.value + '-' + steel_object.max_carbon_value.value]],

        'марганца': [[steel_object.min_marganese_value, steel_object.max_marganese_value],
                     [Steel.min_marganese_value, Steel.max_marganese_value],
                     [steel_object.min_marganese_value.value + '-' + steel_object.max_marganese_value.value]]
    }

    # 1 - defining attribute class
    # 2 - defining steel.attribute object
    # 3 - defining [correct attribute value(s)] for a steel object
    response = {
        SA_OBJ: attribute_dict[attribute_name][0],
        SA_CLASS: attribute_dict[attribute_name][1],
        KEY: attribute_dict[attribute_name][2]
    }

    return response[request_code]


# combine min and max values of the element to create [min1-max1, min2-max2, ...] distractors if it is needed
def generate_min_max_distractors(distractors, attribute):
    if 'в процентах' in attribute.name:
        attribute = attribute.name.split()[2]
        min_max_distractors = {
            'углерода': [steel.min_carbon_value.value + "-" + steel.max_carbon_value.value for steel in distractors],
            'марганца': [steel.min_marganese_value.value + "-" + steel.max_marganese_value.value for steel in
                         distractors]
        }
        return min_max_distractors[attribute]

    else:
        return distractors


# stem, distractors and keys generation manager
def generate_test_item(config):
    config.key_scale_value = define(KEY, config.obj, config.attr.name)

    if config.a_form == 'binary':
        config.final_distractors = ['Да', 'Нет']

        if (config.q_type == 'O>A' or config.q_type == 'A>O') and shorten_generation_process(config):
            return generate_stem(config), config.final_distractors, config.final_key

    generator_manager(config)

    return generate_stem(config), config.final_distractors, config.final_key


def generator_manager(config):
    if config.q_type == 'O>A':
        generate_oa_distractors_and_answers(config)

    elif config.q_type == 'A>O':
        generate_ao_distractors_and_answers(config)

    elif config.q_type == 'O>A>O':
        generate_oao_distractors_and_answers(config)


# Distractors and keys generation for all answer forms (binary, choice, options), for O>A question type
def generate_oa_distractors_and_answers(config):
    steel_object, attribute, key_scale_value = config.obj, config.attr, config.key_scale_value
    distractors = get_scale_values(config)

    if config.a_form == 'binary':
        config.final_key = ['Нет']
        # key is a list, we can handle single and multiple answers
        config.answer_option = random.choice(generate_min_max_distractors(distractors, attribute)).lower()

    # Choice or options
    else:
        distractors = random.sample(distractors, k=4)
        config.scale_value_distractors = generate_min_max_distractors(distractors, attribute)
        config.final_key = config.key_scale_value if config.a_form == 'options' \
            else [random.choice(config.key_scale_value)]

        config.final_distractors = config.final_key + config.scale_value_distractors


# Binary question with positive answer requires only object name and object attribute value, so we can shorten the
# whole generation process
def shorten_generation_process(config):
    if config.a_form == 'binary':
        if config.positive:
            config.answer_option = random.choice(config.key_scale_value).lower()
            config.final_key = ['Да']
            return True
    return False


# Get all scale values from the chosen Scale to use them in distractors
def get_scale_values(config):
    """
    [i.value for i in attribute.values]
    This approach is an appropriate way to work with
    ALL distractors including not existing values and excluding the right answer.
    If we just randomly choose from other objects' values, we will miss a great opportunity to use fake values.
    """
    # defining DB steel object and steel object from request JSON
    db_steel_attribute_value = define(SA_CLASS, config.obj, config.attr.name)
    requested_steel_attribute_value = define(SA_OBJ, config.obj, config.attr.name)
    # Fetching all steel objects except initial steel object OR getting all values from chosen Scale.
    # The key aka correct answer(s) is removed from distractors to avoid random choice uncertainty.
    return session.query(Steel) \
        .filter(Steel.name != config.obj.name,
                db_steel_attribute_value != requested_steel_attribute_value) \
        .all() if 'в процентах' in config.attr.name else list(
        {i.value for i in config.attr.values} - set(config.key_scale_value))


# Distractors and keys generation for all answer forms (binary, choice, options), for A>O question type
def generate_ao_distractors_and_answers(config):
    distractors = get_scale_values(config)

    if config.a_form == 'binary':
        config.final_key = ['Нет']
        # key is a list, we can handle single and multiple answers
        config.answer_option = random.choice(generate_min_max_distractors(distractors, config.attr)).lower()

    else:
        config.answer_option = ', '.join(i for i in config.key_scale_value)
        generate_ao_options(config)


# Get STEEL OBJECTS which can distract or be the right answer
def get_object_possible_answers(config):
    steel_attribute_obj = define(SA_OBJ, config.obj, config.attr.name)
    db_steel_attribute_obj = define(SA_CLASS, config.obj, config.attr.name)

    # this approach was implemented because there is a conflict with SQLAlchemy collection and obj collection comparison
    if 'легир' in config.attr.name:
        object_distractors = [i for i in ALL_STEELS if i.alloying_elements != steel_attribute_obj]
        object_possible_keys = [i for i in ALL_STEELS if
                                i.alloying_elements == steel_attribute_obj and i.name != config.obj.name]

    else:
        # fetch distracting objects
        object_distractors = session.query(Steel) \
            .filter(db_steel_attribute_obj != steel_attribute_obj) \
            .all()

        # fetch valid objects
        object_possible_keys = session.query(Steel) \
            .filter(db_steel_attribute_obj == steel_attribute_obj, Steel.name != config.obj.name) \
            .all()

    return object_distractors, object_possible_keys


# Randomly choose several distractors and right answers from queried steel objects
def generate_ao_options(config):
    object_distractors, object_possible_keys = get_object_possible_answers(config)
    if config.a_form == "choice":
        generate_object_choice(config, [config.obj.name], object_distractors)

    else:
        distractor_num, distractors, possible_keys = shuffle_and_slice(object_distractors, object_possible_keys)
        config.final_key = [config.obj.name] + [steel.name for steel in possible_keys[:4 - distractor_num]]
        config.final_distractors = config.final_key + distractors


# Helpful unit to generate and define distractors and key for CHOICE answer form
def generate_object_choice(config, key, object_distractors):
    config.final_key = key
    random.shuffle(object_distractors)
    distractors_num = 5 if len(key) == 0 else 4
    config.final_distractors = config.final_key + [steel.name for steel in object_distractors[:distractors_num]]


# Helpful unit to shuffle and slice object collections
def shuffle_and_slice(object_distractors, object_possible_keys):
    distractor_num = 5 if len(object_possible_keys) == 0 else random.randint(0, 4)
    random.shuffle(object_distractors)
    random.shuffle(object_possible_keys)
    distractors = [steel.name for steel in object_distractors[:distractor_num]]

    return distractor_num, distractors, object_possible_keys


# Distractors and keys generation for all answer forms (binary, choice, options), for O>A>O question type
def generate_oao_distractors_and_answers(config):
    object_distractors, object_possible_keys = get_object_possible_answers(config)
    distractors = [object_distractors, object_possible_keys]

    if config.a_form == 'binary':
        generate_oao_binary(config, distractors)

    else:
        generate_oao_options(config, distractors)


def generate_oao_binary(config, distractors):
    object_distractors, object_possible_keys = distractors[0], distractors[1]
    config.final_distractors = ['Да', 'Нет']

    config.positive = False if len(object_possible_keys) < 1 else config.positive

    if config.positive:
        config.answer_option = random.choice(object_possible_keys).name
        config.final_key = config.final_distractors[0]

    else:
        config.answer_option = random.choice(object_distractors).name
        config.final_key = config.final_distractors[1]


def generate_oao_options(config, distractors):
    object_distractors, object_possible_keys = distractors[0], distractors[1]

    if config.a_form == 'choice':
        key = object_possible_keys if len(object_possible_keys) == 0 else [random.choice(object_possible_keys).name]
        generate_object_choice(config, key, object_distractors)

    else:
        distractor_num, distractors, possible_keys = shuffle_and_slice(object_distractors, object_possible_keys)
        config.final_key = [steel.name for steel in possible_keys[:5 - distractor_num]]
        config.final_distractors = config.final_key + distractors
