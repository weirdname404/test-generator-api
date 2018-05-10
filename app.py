# coding=utf-8

from flask import Flask
from ontology_db.ontology_parser import parse_ontology

app = Flask(__name__)

if __name__ == '__main__':
    # parse_ontology()
    app.run(debug=True)
