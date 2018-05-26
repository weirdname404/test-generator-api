# coding=utf-8
import random
import uuid

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
ALL_SCALES = session.query(Scale).all()

SA_OBJ = 'steel_attr_obj'
SA_CLASS = 'steel_attr_class'
KEY = 'key'


# main generator func
def generate_test(test_requirements):
    all_tests = []
    # let's check do we support requested question type or not
    for i in test_requirements.request_question_types:
        if i not in ['O>A', 'O>A>O', 'A>O', "A>O>A"]:
            i += ' question type is not supported'
            all_tests.append(i)
            return all_tests

    for _ in range(test_requirements.amount):
        question_type, answer_form, entity_1, entity_2 = make_random_choice(test_requirements)
        steel_object, attribute = define_object_attribute(entity_1, entity_2)
        config = Config(question_type, answer_form, steel_object, attribute)

        # if the answer form is binary, we need to randomly choose will the answer to the Q. be positive or negative
        config.positive = bool(random.getrandbits(1))

        # generate a JSON response form for a single test
        test = generate_json(config)
        test['stem'], test['distractors'], test['key'] = generate_test_item(config)

        all_tests.append(test)

    return all_tests


# randomly choose params from the request
def make_random_choice(test_requirements):
    return random.choice(test_requirements.request_question_types), random.choice(
        test_requirements.request_answer_forms), random.choice(test_requirements.request_entities1), random.choice(
        test_requirements.request_entities2)


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


# TODO
# randomly choose either Scale or Steel object to be compared with initial entity
def choose_entity3(test, entities_list, entity):
    # copy a list, remove the chosen entity, randomly choose new entity
    entities = entities_list[:]
    entities.remove(entity)
    # randomly choose Steel or Scale object
    random_chosen_entity = random.choice(entities)
    test['entity3'] = random_chosen_entity.guid.name

    # if config.a_form == 'binary':
    #     # O>O
    #     # the answer will be positive if the initially chosen Steel object has the same value on the basis
    #     # of chosen Scale with the another randomly chosen Steel object, in other case the answer will be negative
    #     if config.q_type == 'O>O':
    #         config.positive = True if config.key_scale_value == generate_key(random_chosen_entity, config.attr.name) \
    #             else False
    #     # A>A
    #     # the answer will be positive if the initially chosen Object with certain Scale value has also another
    #     # Scale value which was randomly chosen from all Scale values, else - the answer will be negative
    #     elif config.q_type == 'A>A':
    #         random_chosen_scale_value = random.choice(generate_min_max_distractors()random_chosen_entity.values)
    #         config.positive = True if generate_key(config.obj, random_chosen_entity) == random_chosen_scale_value \
    #             else False

    return random_chosen_entity, test


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

        'углерода': [steel_object.min_carbon_value, Steel.min_carbon_value,
                     [steel_object.min_carbon_value.value + '-' + steel_object.max_carbon_value.value]],

        'марганца': [steel_object.min_marganese_value, Steel.min_marganese_value,
                     [steel_object.min_marganese_value.value + '-' + steel_object.max_marganese_value.value]]
    }

    # defining attribute class
    # defining steel.attribute object
    # defining [correct attribute value(s)] for a steel object
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


# generating a stem, distractors and keys
def generate_test_item(config):
    config.key_scale_value = define(KEY, config.obj, config.attr.name)

    if config.a_form == 'binary':
        config.final_distractors = ['Да', 'Нет']

        if (config.q_type == 'O>A' or config.q_type == 'A>O') and shorten_generation_process(config):
            return generate_stem(config), config.final_distractors, config.final_key

    if config.q_type == 'O>A':
        generate_oa_distractors_and_answers(config)

    elif config.q_type == 'A>O':
        generate_ao_distractors_and_answers(config)

    elif config.q_type == 'O>A>O':
        # getting all Steels objects except initial Steel object; shuffling
        # generate entity3 and distractors
        # all_steels = session.query(Steel).filter(Steel.name != steel_object.name).all()
        # random.shuffle(all_steels)
        pass

    elif config.q_type == 'A>O>A':
        pass

    return generate_stem(config), config.final_distractors, config.final_key


# All answer forms for O>A
def generate_oa_distractors_and_answers(config):
    steel_object, attribute, key_scale_value = config.obj, config.attr, config.key_scale_value
    distractors = generate_scale_values_distractors(config)

    if config.a_form == 'binary':
        config.final_key = ['Нет']
        # key is a list, we can handle single and multiple answers
        config.answer_option = random.choice(generate_min_max_distractors(distractors, attribute)).lower()

    else:
        random.shuffle(distractors)
        distractors = distractors[:4]
        config.scale_value_distractors = generate_min_max_distractors(distractors, attribute)
        config.final_key = config.key_scale_value if config.a_form == 'options' \
            else [random.choice(config.key_scale_value)]

        config.final_distractors = config.final_key + config.scale_value_distractors


# For binary question with positive question we need everything we need, so the generation is pointless
def shorten_generation_process(config):
    if config.a_form == 'binary':
        if config.positive:
            config.answer_option = random.choice(config.key_scale_value).lower()
            config.final_key = ['Да']
            return True
    return False


def generate_scale_values_distractors(config):
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


# All answer forms for A>O
def generate_ao_distractors_and_answers(config):
    steel_object, attribute, key_scale_value = config.obj, config.attr, config.key_scale_value
    distractors = generate_scale_values_distractors(config)

    if config.a_form == 'binary':
        config.final_key = ['Нет']
        # key is a list, we can handle single and multiple answers
        config.answer_option = random.choice(generate_min_max_distractors(distractors, attribute)).lower()

    else:
        steel_attribute_obj = define(SA_OBJ, config.obj, config.attr.name)
        db_steel_attribute_obj = define(SA_CLASS, config.obj, config.attr.name)
        config.answer_option = ', '.join(i for i in config.key_scale_value)
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

        if config.a_form == "choice":
            config.final_key = [config.obj.name]
            random.shuffle(object_distractors)
            config.final_distractors = config.final_key + [steel.name for steel in object_distractors[:4]]

        else:
            distractor_num = random.randint(0, 4)
            random.shuffle(object_distractors)
            random.shuffle(object_possible_keys)
            distractors = [steel.name for steel in object_distractors[:distractor_num]]
            config.final_key = [steel_object.name] + [steel.name for steel in object_possible_keys[:4 - distractor_num]]
            config.final_distractors = config.final_key + distractors
