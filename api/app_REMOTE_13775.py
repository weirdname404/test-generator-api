# coding=utf-8
import markdown
from flask import Flask
from flask import Markup
from flask import jsonify, request
from flask_cors import CORS

from api.ontology_db.db_config.base import Base, Session, engine
from api.ontology_db.entities.entity_class import EntityClass
from api.ontology_db.entities.scales import Scale
from api.ontology_db.entities.steel import Steel
from api.ontology_db.ontology_parser import parse_ontology
from api.api_modules.test_generator import generate_test as generate_tests

# creating the Flask application
app = Flask(__name__, template_folder="views")
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


# GET method for fetching all entities (classes, objects, scales)
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


# Welcome message on test-generator-api.herokuapp.com
@app.route('/')
def hello():
    content = """
    Welcome to test generation API.
    ==============================

    Main commands:
    --------------

    /entities - GET method for fetching all classes, objects, and attributes.
    /generate-test - POST method used for test generation. 
    
    Make sure to have the following structure.
    curl -XPOST -H "Content-type: application/json" -d '{"key1": "Value1"}' 'https://test-generator-api.herokuapp.com/generate-test'
    """

    return Markup(markdown.markdown(content))


# POST method for test generation
# a proper request in a JSON format is required
@app.route('/generate-test', methods=['POST'])
def generate_test():
    api_response = {'request_info': request.get_json()}
    test_requirements = api_response['request_info']['test_requirements']

    try:
        amount = test_requirements['count']
        if amount < 0: raise ValueError
        request_question_type = test_requirements['question_type']
        request_answer_form = test_requirements['answer_form']
        request_entities1 = test_requirements['entities1']
        request_entities2 = test_requirements['entities2']

        app.logger.info("\nArguments: %s %s %s %s %s" % (
        amount, request_question_type, request_answer_form, request_entities1, request_entities2))

    except KeyError as e:
        return '\nThe key %s does not exits!\n' % str(e), 400

    except ValueError as e:
        return '\nThe amount of questions cannot be < 0\n', 400

    api_response['questions'] = generate_tests(amount, request_question_type, request_answer_form, request_entities1,
                                               request_entities2)

    return jsonify(api_response)


if __name__ == '__main__':
    app.run(debug=True)
