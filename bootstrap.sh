#!/bin/sh
export FLASK_APP=./api/app.py
export FLASK_ENV=development
flask run -h 0.0.0.0
