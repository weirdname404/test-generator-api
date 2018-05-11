# coding=utf-8

from flask import Flask, jsonify, request

from api.ontology_db.entities.db_config.base import Base, Session, engine
from api.ontology_db.entities.scales import Scale
from api.ontology_db.entities.steel import Steel
from api.ontology_db.entities.entity_class import EntityClass
from api.ontology_db.ontology_parser import parse_ontology

# creating the Flask application
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# if needed, generate database schema
Base.metadata.create_all(engine)


@app.route("/update-ontology")
def get_ontology():
    parse_ontology()
    return "Ontology was successfully parsed.\nData was moved to DB."


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

    # # transforming into JSON-serializable objects
    # schema = ResponseEntitiesSchema(many=True)
    # entities = schema.dump(objects)

    # serializing as JSON
    return jsonify(entities)


if __name__ == '__main__':
    app.run(debug=True)
