# coding=utf-8

from flask import Flask, jsonify, request
from flask_cors import CORS

from api.ontology_db.db_config.base import Base, Session, engine
from api.ontology_db.entities.scales import Scale
from api.ontology_db.entities.steel import Steel
from api.ontology_db.entities.entity_class import EntityClass
from api.ontology_db.ontology_parser import parse_ontology

# creating the Flask application
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# if needed, generate database schema
Base.metadata.create_all(engine)

sample = {"questions": [{
    "guid": "Q1_GUID",
    "question_type": "O>A",
    "answer_form": "choice",
    "entity1": "E1_GUID",
    "entity2": "E2_GUID",
    "stem": "Определите верный способ раскисления у марки стали 05кп:",
    "distractors": [
        "Полуспокойная",
        "Кипящая",
        "Спокойная"
    ],

    "key": [1]
}]}


@app.route("/update-ontology")
def get_ontology():
    parse_ontology()
    return "Ontology was successfully parsed.\nData was moved to DB.\n"


@app.route('/entities')
def get_entities():
    # fetching from the database
    session = Session()
    steel_objs = session.query(Steel).all()
    scale_objs = session.query(Scale).all()
    class_objs = session.query(EntityClass).distinct().all()
    session.close()

    objects = [steel.name for steel in steel_objs]
    scales = [scale.name for scale in scale_objs]
    classes = [entity_class.name for entity_class in class_objs]

    entities = {'Objects': objects, 'Attributes': scales, 'Classes': classes}

    return jsonify(entities)


@app.route('/')
def hello():
    return "Hello user! Welcome to test generation API."

@app.route('/generate-test', methods=['POST'])
def generate_test():
    user_request = {'request_info': request.get_json()}

    return jsonify(user_request, sample)


if __name__ == '__main__':
    app.run(debug=True)
