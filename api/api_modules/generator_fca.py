# coding=utf-8
import random
import time
import uuid
from concepts import Context
from api.api_modules.generator_modules.generation_config import Config
from api.api_modules.generator import make_random_choice

context = Context.fromfile('./binary_context.csv', frmat='csv')
scales_context = Context.fromfile('./scales_context.csv', frmat='csv')
ALL_STEELS = context.objects
ALL_ATTRS = context.properties


# main generator func
def generate_test_fca(test_requirements):
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
        config.obj2, config.attr2 = entity_1, entity_2
        config.steel_attributes = context.intension([config.obj2])
        scale_attributes = list(scales_context.intension([config.attr2]))
        config.support_index = int(scale_attributes.pop())
        config.scale_attributes = scale_attributes

        # if the answer form is binary, we need to randomly choose will the answer to the Q. be positive or negative
        config.positive = bool(random.getrandbits(1))

        # generate a JSON response form for a single test
        test = generate_json(config)
        test['stem'], test['distractors'], test['key'] = generate_test_item(config)

        all_tests.append(test)

    print(f"--- {time.time() - start_time} seconds ---")

    return all_tests


def generate_json(config):
    test = {'guid': str(uuid.uuid4()).upper(), 'question_type': config.q_type, 'answer_form': config.a_form,
            'entity1': ''
            if config.q_type == 'O>A' or config.q_type == 'O>A>O' else config.attr.guid.name,
            'entity2': ''
            if config.q_type == 'O>A' or config.q_type == 'O>A>O' else config.obj.guid.name}

    return test


def generate_test_item(config):
    if config.a_form == 'binary':
        config.final_distractors = ['Да', 'Нет']
        if config.positive:
            config.final_key = ['Да']
            support_index = config.support_index
            config.answer_option = (config.steel_attributes[support_index] if support_index != 4 else random.choice(
                config.steel_attributes[4:])).lower()

        else:
            chosen_attribute = random.choice(config.scale_attributes)
            config.final_key = ['Да'] if chosen_attribute in config.steel_attributes else ['Нет']
            config.answer_option = chosen_attribute.lower()

    return generate_stem(config), config.final_distractors, config.final_key


def generate_stem(config):
    stems = {
        'Способ раскисления': f"Верно ли, что сталь {config.obj2} по способу раскисления {config.answer_option}?",

        'Содержание легирующих элементов': f"Содержит ли сталь {config.obj2} {config.answer_option} " +
                                           "в качестве легирующего элемента?",

        'Характеристика качества': f"Верно ли, что сталь {config.obj2} {config.answer_option}?",

        'ГОСТ сплава': f"Входит ли сталь {config.obj2} входит в {config.answer_option.upper()}?"
    }

    return stems[config.attr2]
