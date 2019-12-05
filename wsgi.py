#!/usr/bin/env python

from os import environ
from app import create_app


class Config:
    TESTING = False
    FLASK_DEBUG = environ.get('FLASK_DEBUG')
    SECRET_KEY = environ.get('SECRET_KEY')

    # database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    # password hashing
    BCRYPT_LOG_ROUNDS = int(environ.get('BCRYPT_LOG_ROUNDS', 15))


app = create_app(Config)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
