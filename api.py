#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api, Resource, url_for
from resources.test_generator import Test

app = Flask(__name__)
api = Api(app)

api.add_resource(Test, '/response')

if __name__ == '__main__':
    app.run(debug=True)