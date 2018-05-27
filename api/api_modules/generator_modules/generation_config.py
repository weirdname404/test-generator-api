# coding=utf-8

from api.ontology_db.entities.scales import Scale
from api.ontology_db.entities.steel import Steel


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

    def __init__(self, q_type, a_form):
        self.q_type = q_type
        self.a_form = a_form
