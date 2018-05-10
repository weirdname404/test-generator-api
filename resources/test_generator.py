# coding=utf-8

import json


class Test(Resource):
    def get(self):
        # just open the file...
        # read the file and decode possible UTF-8 signature at the beginning
        # which can be the case in some files.
        with open("resources/ontology.json", 'r', encoding='utf8') as json_file:
            # str -> dict
            data = json.load(json_file)

        # return json.dumps(data, encoding='utf-8')
        return json.dumps(data, ensure_ascii=False)
        # return data

    def post(self):
        pass