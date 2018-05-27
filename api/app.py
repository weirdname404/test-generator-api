# coding=utf-8
import markdown
from flask import Flask
from flask import jsonify, request
from flask_cors import CORS

from api.ontology_db.db_config.base import Base, Session, engine
from api.ontology_db.entities.entity_class import EntityClass
from api.ontology_db.entities.scales import Scale
from api.ontology_db.entities.steel import Steel
from api.ontology_db.ontology_parser import parse_ontology, drop_ontology as drop_onto
from api.api_modules.generator import generate_test as generate_tests
from api.api_modules.requirements_class import TestRequirements

# creating the Flask application
app = Flask(__name__, template_folder="views")
app.config['JSON_AS_ASCII'] = False
CORS(app)

# if needed, generate database schema
Base.metadata.create_all(engine)

session = Session()
# fetching entity names from the database
steels = [steel.name for steel in session.query(Steel).all()]
scales = [scale.name for scale in session.query(Scale).all()]
classes = [entity_class.name for entity_class in session.query(EntityClass).distinct().all()]
session.close()

last_successful_request = """
curl -XPOST -H "Content-type: application/json" -d '{"author": 
"Author","creation_date": "01.01.1970","version": "1.00","guid": "2E7E22F4-5B51-4948-B120-AB21F08317DB",
"test_requirements": {"count": 100,"question_type": ["O>A>O", "O>A", "A>O"],
"answer_form": ["binary", "choice", "options"],"entities1": ["Ст4сп", "05кп", "50", "20", "60"],
"entities2": ["Содержание легирующих элементов", "Способ раскисления", 
"Характеристика качества", "ГОСТ сплава", "Максимальная доля углерода в процентах", 
"Минимальная доля марганца в процентах"]}}' 'test-generator-api.herokuapp.com/generate-test'"""


@app.route("/update-ontology")
def get_ontology():
    parse_ontology()
    return "Ontology was successfully parsed.\nData was moved to DB.\n"


@app.route("/drop-ontology")
def drop_ontology():
    drop_onto()
    return "Ontology DB was dropped.\n"


# GET method for fetching all entities (classes, objects, scales)
@app.route('/entities')
def get_entities():
    return jsonify({'Objects': steels, 'Attributes': scales, 'Classes': classes})


# Welcome message on test-generator-api.herokuapp.com
@app.route('/')
def hello():
    return """<h3>Welcome to Educational Test Item Generation API</h3>
    <p><b>Main commands:</b><br>
    /entities - <i>GET method for fetching all classes, objects, and attributes.</i><br>
    /generate-test - <i>POST method which is used to send a request for test generation.</i></p><br>
    <b>JSON structure should be similar to the example below:</b><br>
     <code>{"author": "Author","creation_date": "01.01.1970",</code><br>
     <code>"version": "1.00","guid": "2E7E22F4-5B51-4948-B120-AB21F08317DB",</code><br>
     <code>"test_requirements": {"count": 5,"question_type": ["O>A"],</code><br>
     <code>"answer_form": ["binary"],"entities1": ["Ст4сп", "05кп"],"entities2": 
     ["Максимальная доля углерода в процентах", "ГОСТ сплава"]}}</code><br><br><br>
     <b>Last successful request via terminal:</b><br><code> %s </code><br><br>""" % last_successful_request


# POST method for test generation
# a proper request in a JSON format is required
@app.route('/generate-test', methods=['POST'])
def generate_test():
    try:
        api_response = {'request_info': request.get_json()}
        test_requirements_json = api_response['request_info']['test_requirements']
        if test_requirements_json['count'] < 0:
            raise ValueError

        test_requirements = TestRequirements(test_requirements_json['count'], test_requirements_json['question_type'],
                                             test_requirements_json['answer_form'])

        error_value = check_entities(test_requirements_json['entities1'], test_requirements_json['entities2'])
        if error_value:
            raise TypeError

        else:
            test_requirements.request_entities1 = test_requirements_json['entities1']
            test_requirements.request_entities2 = test_requirements_json['entities2']

        # TODO Add Logging

    except KeyError as e:
        return f'\nThe key {e} does not exits!\n', 400

    except ValueError as e:
        return '\nThe amount of questions cannot be < 0\n', 400

    except TypeError:
        return f'\nThe request is invalid. {error_value} does not exist in the ontology\n', 400

    api_response['questions'] = generate_tests(test_requirements)

    return jsonify(api_response)


# the user could make a mistake so we should check before generation
def check_entities(request_entities1, request_entities2):
    all_entities = set(steels + scales + classes)
    request_entities = request_entities1 + request_entities2
    for entity in request_entities:
        if entity not in all_entities:
            return entity
    return False


if __name__ == '__main__':
    app.run(debug=True)
