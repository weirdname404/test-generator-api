# coding=utf-8

import random


def generate_stem(config):
    if config.q_type == 'O>A':
        stem = generate_oa_stem(config)

    elif config.q_type == 'A>O':
        stem = generate_ao_stem(config)

    elif config.q_type == 'O>A>O':
        stem = generate_oao_stem(config)

    else:
        stem = ''

    return stem


def generate_oa_stem(config):
    attribute, answer_option = config.attr, config.answer_option
    stems = {
        'binary': {
            'Способ раскисления': f"Верно ли, что сталь {config.obj.name} по способу раскисления {answer_option}?",

            'Содержание легирующих элементов': f"Содержит ли сталь {config.obj.name} {answer_option} " +
                                               "в качестве легирующего элемента?",

            'Характеристика качества': f"Верно ли, что сталь {config.obj.name} {answer_option}?",

            'ГОСТ сплава': f"Входит ли сталь {config.obj.name} в {answer_option.upper()}?"
        },
        'choice&options': {
            'Способ раскисления': f"Охарактеризуйте с точки зрения способа раскисления сталь {config.obj.name}:",

            'Содержание легирующих элементов': f"{generate_synonym('verb')} один или несколько легирующих " +
                                               f"элементов, которые входят в состав стали {config.obj.name}:",

            'Характеристика качества': f"{generate_synonym('verb')} характеристику качества стали {config.obj.name}:",

            'ГОСТ сплава': f"{generate_synonym('verb')} к какому ГОСТу относится сталь {config.obj.name}:"
        }
    }

    if config.a_form == 'binary':
        if 'доля' in attribute.name:
            stem = f"Верно ли, что массовая доля {attribute.name.split()[2]} у стали " + \
                   f"{config.obj.name} равна {answer_option}%?"
        else:
            stem = stems[config.a_form][attribute.name]

    # Options or Choice
    else:
        if 'доля' in attribute.name:
            stem = f"{generate_synonym('verb')} какая массовая доля {attribute.name.split()[2]} в процентах у " + \
                   f"стали {config.obj.name}:"
        else:
            stem = stems['choice&options'][attribute.name]

    return stem


def generate_ao_stem(config):
    return get_ao_binary_stem(config) if config.a_form == 'binary' else get_ao_else_stem(config)


def get_ao_binary_stem(config):
    question_start = 'Согласны ли Вы с тем, что верным примером стали,'
    attribute, answer_option = config.attr, config.answer_option

    if attribute.name == 'Способ раскисления':
        stem = f"{question_start} которую по способу раскисления можно охарактеризовать как " + \
               f"{answer_option[:-2]}ую, является сталь {config.obj.name}?"

    elif attribute.name == 'Содержание легирующих элементов':
        stem = f"{question_start} которая содержит {answer_option} в качестве легирующего элемента, является " + \
               f"сталь {config.obj.name}?"

    elif attribute.name == 'Характеристика качества':
        stem = f"{question_start} которую можно охарактеризовать как сталь {answer_option}, является сталь " + \
               f"марки {config.obj.name}?"

    elif attribute.name == 'ГОСТ сплава':
        stem = f"{question_start} которая входит в {answer_option.upper()}, является сталь {config.obj.name}?"

    else:
        stem = f"{question_start} массовая доля {attribute.name.split()[2]} которой равна {answer_option}%, " + \
               f"является сталь {config.obj.name}?"

    return stem


def get_ao_else_stem(config):
    attribute, answer_option = config.attr, config.answer_option
    if attribute.name == 'Способ раскисления':
        stem = f"{generate_synonym('verb')} марки стали, каждую из которых можно охарактеризовать по способу " + \
               f"раскисления как {answer_option[:-2].lower()}" + "ую:"

    elif attribute.name == 'Содержание легирующих элементов':
        stem = f"{generate_synonym('verb')} марки стали, состав которых содержит следующие легирующие элементы" + \
               f" - {answer_option}:"

    elif attribute.name == 'Характеристика качества':
        stem = f"Сталь {answer_option.lower()}. {generate_synonym('verb')} марки стали, которые соответсвуют " + \
               "данной характеристике:"

    elif attribute.name == 'ГОСТ сплава':
        stem = f"{generate_synonym('verb')} марки стали, которые входят в {answer_option}:"

    else:
        stem = f"{generate_synonym('verb')} марки стали, у которых массовая доля {attribute.name.split()[2]} " + \
               f"равна {answer_option}%:"

    return stem


def generate_oao_stem(config):
    return get_oao_binary_stem(config) if config.a_form == 'binary' else get_oao_else_stem(config)


def get_oao_binary_stem(config):
    attribute, answer_option = config.attr, config.answer_option
    start = 'Верно ли, что сталь'

    if attribute.name == 'Способ раскисления':
        stem = f"{start} {config.obj.name} одинакова по способу раскисления со сталью {answer_option}?"

    elif attribute.name == 'Содержание легирующих элементов':
        stem = f"{start} {config.obj.name} одинакова по содержанию легирующих элементов со сталью {answer_option}?"

    elif attribute.name == 'Характеристика качества':
        stem = f"{start} {config.obj.name} одинакова по характеристике качества со сталью {answer_option}?"

    elif attribute.name == 'ГОСТ сплава':
        stem = f"{start} {config.obj.name} входит в тот же ГОСТ, что и сталь {answer_option}?"

    else:
        stem = f"{start} {config.obj.name} равна по массовой доле {attribute.name.split()[2]} со сталью " + \
               f"{answer_option}?"

    return stem


def get_oao_else_stem(config):
    attribute, answer_option = config.attr, config.answer_option

    if attribute.name == 'Способ раскисления':
        stem = f"{generate_synonym('verb')} марки стали, которые по способу раскисления одинаковы со сталью " + \
               f"{config.obj.name}:"

    elif attribute.name == 'Содержание легирующих элементов':
        stem = f"{generate_synonym('verb')} марки стали, которые по содержанию легирующих элементов одинаковы со " + \
               f"сталью {config.obj.name}:"

    elif attribute.name == 'Характеристика качества':
        stem = f"{generate_synonym('verb')} марки стали, которые по характеристике качества одинаковы со сталью " + \
               f"{config.obj.name}:"

    elif attribute.name == 'ГОСТ сплава':
        stem = f"{generate_synonym('verb')} марки стали, которые входят в тот же ГОСТ, что и сталь {config.obj.name}:"

    else:
        stem = f"{generate_synonym('verb')} марки стали, которые по массовой доле {attribute.name.split()[2]} " + \
               f"одинаковы со сталью {config.obj.name}:"

    return stem


def generate_synonym(word):
    verb = ['Определите', 'Укажите', 'Выберите', 'Назовите']
    adjective = []
    word_dict = {'verb': verb, 'adj': adjective}
    return random.choice(word_dict[word])

# def get_anything_stem(config):
#     attribute, answer_option = config.attr, config.answer_option
#
#     if attribute.name == 'Способ раскисления':
#         stem = f""
#
#     elif attribute.name == 'Содержание легирующих элементов':
#         stem = f""
#
#     elif attribute.name == 'Характеристика качества':
#         stem = f""
#
#     elif attribute.name == 'ГОСТ сплава':
#         stem = f""
#
#     else:
#         stem = f""
#
#     return stem
