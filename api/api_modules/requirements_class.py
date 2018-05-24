# coding=utf-8

class TestRequirements:
    amount = 0
    request_question_types = ''
    request_answer_forms = ''
    request_entities1 = ''
    request_entities2 = ''

    def __init__(self, amount, request_question_types, request_answer_forms):
        self.amount = amount
        self.request_question_types = request_question_types
        self.request_answer_forms = request_answer_forms
