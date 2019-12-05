#!/usr/bin/env python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt import JWT

db = SQLAlchemy()
ma = Marshmallow()
bc = Bcrypt()
jwt = JWT()


def create_app(config):
    from .store import UserStore, auth_response
    """Constructs the core application."""
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    ma.init_app(app)
    bc.init_app(app)

    # because of flask JWT, it expects to receive the auth handler in
    # its constructor
    user_store = UserStore(db)
    jwt.authentication_callback = user_store.check_login
    jwt.identity_callback = user_store.get_user_by_token_claim
    jwt.auth_response_callback = auth_response
    jwt.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()
        return app
