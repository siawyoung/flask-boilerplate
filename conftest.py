#!/usr/bin/env python

import pytest
import testing.postgresql

from app import create_app, db as _db


class TestConfig:
    FLASK_DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "test"
    TESTING = True
    SECRET_KEY = "testing-secret"
    with testing.postgresql.Postgresql(port=5432) as postgresql:
        SQLALCHEMY_DATABASE_URI = postgresql.url()


@pytest.yield_fixture(scope="session")
def app():
    _app = create_app(TestConfig)
    ctx = _app.app_context()
    ctx.push()
    yield _app
    ctx.pop()


@pytest.fixture(scope="session")
def testapp(app):
    return app.test_client()


@pytest.yield_fixture(scope="session")
def db(app):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()
