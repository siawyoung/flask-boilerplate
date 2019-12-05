#!/usr/bin/env bash

export TESTING=True
export FLASK_ENV=development
export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
export SQLALCHEMY_DATABASE_URI=postgres://localhost:5432/flask-boilerplate
export SQLALCHEMY_TRACK_MODIFICATIONS=False
export BCRYPT_LOG_ROUNDS=15
export SECRET_KEY=hello
flask run
