# coding=utf-8

from api.ontology_db.entities.scales import Scale
from api.ontology_db.entities.steel import Steel


# generator func takes lots of args, that's why special config class was created
class Config:

    def __init__(self, q_type, a_form):
        self.q_type = q_type
        self.a_form = a_form
        self.obj = Steel
        self.attr = Scale
        self.key_scale_value = []
        self.key_object_value = []
        self.object_distractors = []
        self.scale_value_distractors = []
        self.positive = True
        self.answer_option = ''
        self.obj2 = Steel
        self.attr2 = Scale
        self.final_key = []
        self.final_distractors = []
