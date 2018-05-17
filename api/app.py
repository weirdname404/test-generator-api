# coding=utf-8
import markdown
from flask import Flask
from flask import jsonify, request
from flask_cors import CORS

from api.ontology_db.db_config.base import Base, Session, engine
from api.ontology_db.entities.entity_class import EntityClass
from api.ontology_db.entities.scales import Scale
from api.ontology_db.entities.steel import Steel
from api.ontology_db.ontology_parser import parse_ontology, drop_tables
from api.api_modules.test_generator import generate_test as generate_tests

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


@app.route("/drop-ontology")
def drop_ontology():
    drop_tables(session)
    return "DB was dropped.\n"


# GET method for fetching all entities (classes, objects, scales)
@app.route('/entities')
def get_entities():
    return jsonify({'Objects': steels, 'Attributes': scales, 'Classes': classes})


# Welcome message on test-generator-api.herokuapp.com
@app.route('/')
def hello():
    content = """
    <h3>Welcome to test generation API</h3>
    <p><b>Main commands:</b><br><br>
    /entities - <i>GET method for fetching all classes, objects, and attributes.</i><br>
    /generate-test - <i>POST method which is used to send a request for test generation.</i></p>
    <b>Make sure to have the following structure of a request:</b>
    <code> curl -XPOST -H "Content-type: application/json" -d '{"key1": "Value1"}' 
    'https://test-generator-api.herokuapp.com/generate-test'</code><br><br><br>
    <b>JSON structure should be similar to the example below:</b><br><br>
     <code>{"author": "Author","creation_date": "01.01.1970",</code><br>
     <code>"version": "1.00","guid": "2E7E22F4-5B51-4948-B120-AB21F08317DB",</code><br>
     <code>"test_requirements": {"count": 5,"question_type": ["O>A"],</code><br>
     <code>"answer_form": ["binary"],"entities1": ["Ст4сп", "05кп"],"entities2": 
     ["Максимальная доля углерода в процентах", "ГОСТ сплава"]}}</code><br>
    """
    return content


# POST method for test generation
# a proper request in a JSON format is required
@app.route('/generate-test', methods=['POST'])
def generate_test():
    try:
        api_response = {'request_info': request.get_json()}
        test_requirements = api_response['request_info']['test_requirements']
        amount = test_requirements['count']
        if amount < 0:
            raise ValueError

        request_question_type = test_requirements['question_type']
        request_answer_form = test_requirements['answer_form']
        request_entities1 = test_requirements['entities1']
        request_entities2 = test_requirements['entities2']
        error_value = ''
        error_value = check_entities(request_entities1, request_entities2)
        if error_value:
            raise TypeError

        app.logger.info("\nArguments: %s %s %s %s %s" % (
            amount, request_question_type, request_answer_form, request_entities1, request_entities2))

    except KeyError as e:
        return '\nThe key %s does not exits!\n' % e, 400

    except ValueError as e:
        return '\nThe amount of questions cannot be < 0\n', 400

    except TypeError:
        return '\nThe request is invalid. %s does not exist in the ontology\n' % (error_value), 400

    api_response['questions'] = generate_tests(amount, request_question_type, request_answer_form, request_entities1,
                                               request_entities2)

    return jsonify(api_response)


# the user could make a mistake so we should check before generation
def check_entities(request_entities1, request_entities2):
    all_entities = steels + scales + classes
    request_entities = request_entities1 + request_entities2
    print(all_entities, request_entities)
    for entity in request_entities:
        if entity not in all_entities:
            return entity
    return False


if __name__ == '__main__':
    app.run(debug=True)
