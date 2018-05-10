# coding=utf-8

from flask import Flask
from api.ontology_db.ontology_parser import parse_ontology

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == '__main__':
    parse_ontology()
    app.run(debug=True)
