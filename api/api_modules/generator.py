# coding=utf-8
import random
import uuid

from api.ontology_db.db_config.base import Base, Session, engine
from api.ontology_db.entities.scales import Scale
from api.ontology_db.entities.steel import Steel

# connect to DB
Base.metadata.create_all(engine)
session = Session()

# constants
ALL_STEELS = session.query(Steel).all()
ALL_SCALES = session.query(Scale).all()


# generator func takes lots of args, that's why special config class was created
class Config:
    q_type = ''
    a_form = ''
    obj = Steel
    attr = Scale
    key_scale_value = []
    key_object_value = []
    object_distractors = []
    scale_value_distractors = []
    positive = True
    answer_option = ''
    obj2 = Steel
    attr2 = Scale
    final_key = []
    final_distractors = []

    def __init__(self, q_type, a_form, ent1, ent2):
        self.q_type = q_type
        self.a_form = a_form
        self.obj = ent1
        self.attr = ent2


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
    steel_object = session.query(Steel).filter(Steel.name == steel_object).all()
    attribute = session.query(Scale).filter(Scale.name == attribute).all()

    return steel_object[0], attribute[0]


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


# defining [correct attribute value(s)] for a steel object
def generate_key(steel_object, attribute_name):
    if 'в процентах' in attribute_name:
        attribute_name = attribute_name.split()[2]

    relations_dict = {
        'Способ раскисления': [steel_object.deoxidizing_type.name],
        'Содержание легирующих элементов': [i.name for i in steel_object.alloying_elements],
        'Характеристика качества': [steel_object.quality.name],
        'ГОСТ сплава': [steel_object.gost.name],
        'углерода': [steel_object.min_carbon_value.value + '-' + steel_object.max_carbon_value.value],
        'марганца': [steel_object.min_marganese_value.value + '-' + steel_object.max_marganese_value.value]
    }

    return relations_dict[attribute_name]


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
    config.key_scale_value = generate_key(config.obj, config.attr.name)
    binary = True if config.a_form == 'binary' else False
    stem = ''

    if config.q_type == 'O>A':
        generate_oa_distractors_and_answers(config)
        stem = generate_oa_stem(binary, config.obj, config.attr, config.answer_option, stem)

    elif config.q_type == 'A>O':
        pass

    elif config.q_type == 'O>A>O':
        # getting all Steels objects except initial Steel object; shuffling
        # generate entity3 and distractors
        # all_steels = session.query(Steel).filter(Steel.name != steel_object.name).all()
        # random.shuffle(all_steels)
        pass

    elif config.q_type == 'A>O>A':
        pass

    return stem, config.final_distractors, config.final_key


# All answer forms for O>A
def generate_oa_distractors_and_answers(config):
    steel_object, attribute, key_scale_value = config.obj, config.attr, config.key_scale_value
    # Case to shorten the generation process
    if config.a_form == 'binary':
        config.final_distractors = ['Да', 'Нет']
        if config.positive:
            config.answer_option = random.choice(config.key_scale_value).lower()
            config.final_key = ['Да']
            return

    # Fetching all steel objects except initial steel object OR getting all values from chosen Scale.
    # The key aka correct answer(s) is removed from distractors to avoid random choice uncertainty.
    distractors = session.query(Steel).filter(
        Steel.name != steel_object.name,
        Steel.min_carbon_value != steel_object.min_carbon_value).all() if 'в процентах' in attribute.name \
        else list({i.value for i in attribute.values} - set(key_scale_value))

    """ 
    [i.value for i in attribute.values]
    This approach is an appropriate way to work with 
    ALL distractors including not existing values and excluding the right answer.
    If we just randomly choose from other objects' values, we will miss a great opportunity to use fake values.
    """

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


def generate_oa_stem(binary, steel_object, attribute, answer_option, stem):
    if binary:
        if attribute.name == 'Способ раскисления':
            stem += f"Верно ли, что сталь {steel_object.name} по способу раскисления {answer_option}?"

        elif attribute.name == 'Содержание легирующих элементов':
            stem += f"Содержит ли сталь {steel_object.name} {answer_option} в качестве легирующего элемента?"

        elif attribute.name == 'Характеристика качества':
            stem += f"Верно ли, что сталь {steel_object.name} {answer_option}?"

        elif attribute.name == 'ГОСТ сплава':
            stem += f"Входит ли сталь {steel_object.name} в {answer_option.upper()}?"

        else:
            stem += f"Верно ли, что массовая доля {attribute.name.split()[2]} у стали " + \
                    f"{steel_object.name} равна {answer_option}%?"

    # Options or Choice
    else:
        if attribute.name == 'Способ раскисления':
            stem += f"Охарактеризуйте с точки зрения способа раскисления сталь {steel_object.name}:"

        elif attribute.name == 'Содержание легирующих элементов':
            stem += f"{generate_synonym('verb')} один или несколько легирующих элементов, которые " + \
                    f"входят в состав стали {steel_object.name}:"

        elif attribute.name == 'Характеристика качества':
            stem += f"Сталь {steel_object.name} можно охарактеризовать с точки зрения качества как:"

        elif attribute.name == 'ГОСТ сплава':
            stem += f"{generate_synonym('verb')} к какому ГОСТу относится сталь {steel_object.name}:"

        else:
            stem += f"{generate_synonym('verb')} какая массовая доля {attribute.name.split()[2]} в процентах у " + \
                    f"стали {steel_object.name}:"

    return stem


def generate_synonym(word):
    verb = ['Определите', 'Укажите', 'Выберите', 'Назовите']
    adjective = []
    word_dict = {'verb': verb, 'adj': adjective}
    return random.choice(word_dict[word])
