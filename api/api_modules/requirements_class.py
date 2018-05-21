# coding=utf-8

class TestRequirements:
    amount = 0
    request_question_types = ''
    request_answer_forms = ''
    request_entities1 = ''
    request_entities2 = ''

    def __init__(self, amount, request_question_types):
        self.amount = amount
        self.request_question_types = request_question_types
