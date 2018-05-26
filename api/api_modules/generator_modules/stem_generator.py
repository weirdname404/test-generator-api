# coding=utf-8

import random


def generate_stem(config):
    stem = ''

    if config.q_type == 'O>A':
        stem = generate_oa_stem(config)

    elif config.q_type == 'A>O':
        stem = generate_ao_stem(config)

    elif config.q_type == 'O>A>O':
        pass

    else:
        pass

    return stem


def generate_oa_stem(config):
    stem = ''
    binary, attribute, answer_option = True if config.a_form == 'binary' else False, config.attr, config.answer_option

    if binary:
        if attribute.name == 'Способ раскисления':
            stem += f"Верно ли, что сталь {config.obj.name} по способу раскисления {answer_option}?"

        elif attribute.name == 'Содержание легирующих элементов':
            stem += f"Содержит ли сталь {config.obj.name} {answer_option} в качестве легирующего элемента?"

        elif attribute.name == 'Характеристика качества':
            stem += f"Верно ли, что сталь {config.obj.name} {answer_option}?"

        elif attribute.name == 'ГОСТ сплава':
            stem += f"Входит ли сталь {config.obj.name} в {answer_option.upper()}?"

        else:
            stem += f"Верно ли, что массовая доля {attribute.name.split()[2]} у стали " + \
                    f"{config.obj.name} равна {answer_option}%?"

    # Options or Choice
    else:
        if attribute.name == 'Способ раскисления':
            stem += f"Охарактеризуйте с точки зрения способа раскисления сталь {config.obj.name}:"

        elif attribute.name == 'Содержание легирующих элементов':
            stem += f"{generate_synonym('verb')} один или несколько легирующих элементов, которые " + \
                    f"входят в состав стали {config.obj.name}:"

        elif attribute.name == 'Характеристика качества':
            stem += f"{generate_synonym('verb')} характеристику качества стали {config.obj.name}:"

        elif attribute.name == 'ГОСТ сплава':
            stem += f"{generate_synonym('verb')} к какому ГОСТу относится сталь {config.obj.name}:"

        else:
            stem += f"{generate_synonym('verb')} какая массовая доля {attribute.name.split()[2]} в процентах у " + \
                    f"стали {config.obj.name}:"

    return stem


def generate_ao_stem(config):
    stem = ''
    question_start = 'Согласны ли Вы с тем, что верным примером стали,'
    binary, attribute, answer_option = True if config.a_form == 'binary' else False, config.attr, config.answer_option

    if binary:
        if attribute.name == 'Способ раскисления':
            stem += f"{question_start} которую по способу раскисления можно охарактеризовать как " + \
                    f"{answer_option[:-2]}ую, является сталь {config.obj.name}?"

        elif attribute.name == 'Содержание легирующих элементов':
            stem += f"{question_start} которая содержит {answer_option} в качестве легирующего элемента, является " + \
                    f"сталь {config.obj.name}?"

        elif attribute.name == 'Характеристика качества':
            stem += f"{question_start} которую можно охарактеризовать как сталь {answer_option}, является сталь " + \
                    f"марки {config.obj.name}?"

        elif attribute.name == 'ГОСТ сплава':
            stem += f"{question_start} которая входит в {answer_option.upper()}, является сталь {config.obj.name}?"

        else:
            stem += f"{question_start} массовая доля {attribute.name.split()[2]} которой равна {answer_option}%, " + \
                    f"является сталь {config.obj.name}?"

    # Options or Choice
    else:
        if attribute.name == 'Способ раскисления':
            stem += f"{generate_synonym('verb')} марки стали, каждую из которых можно охарактеризовать по способу " + \
                    f"раскисления как {answer_option[:-2].lower()}" + "ую:"

        elif attribute.name == 'Содержание легирующих элементов':
            stem += f"{generate_synonym('verb')} марки стали, состав которых содержит следующие легирующие элементы" + \
                    f" - {answer_option}:"

        elif attribute.name == 'Характеристика качества':
            stem += f"Сталь {answer_option.lower()}. {generate_synonym('verb')} марки стали, которые соответсвуют " + \
                    "данной характеристике:"

        elif attribute.name == 'ГОСТ сплава':
            stem += f"{generate_synonym('verb')} марки стали, которые входят в {answer_option}:"

        else:
            stem += f"{generate_synonym('verb')} марки стали, у которых массовая доля {attribute.name.split()[2]} " + \
                    f"равна {answer_option}%:"

    return stem


def generate_synonym(word):
    verb = ['Определите', 'Укажите', 'Выберите', 'Назовите']
    adjective = []
    word_dict = {'verb': verb, 'adj': adjective}
    return random.choice(word_dict[word])
