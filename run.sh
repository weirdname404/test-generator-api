#!/bin/sh
#!/usr/bin/env python
export FLASK_APP=./api/app.py
export FLASK_ENV=development
python -c "from api.app import parse_ontology; parse_ontology()"
flask run -h 0.0.0.0
