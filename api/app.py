# coding=utf-8

from flask import Flask
from api.ontology_db.ontology_parser import parse_ontology

app = Flask(__name__)


@app.route("/parse_ontology")
def hello_world():
    parse_ontology()
    return "Ontology was successfully parsed.\nData was moved to DB."


if __name__ == '__main__':
    app.run(debug=True)
