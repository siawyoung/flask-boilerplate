#!/usr/bin/env python

import json
from app import db
from app.models import User
from .utils import random_email


class UserFactory:
    def __init__(self):
        self.counter = 0

    @staticmethod
    def get_password(user):
        return "{}_password".format(user.username)

    def create_user(self, testapp):
        username = "user_{}".format(str(self.counter))
        password = "{}_password".format(username)
        email = random_email()
        self.counter += 1
        return User(username=username, password=password, email=email)


user_factory = UserFactory()


def create_user(testapp):
    user = user_factory.create_user(testapp)
    db.session.add(user)
    db.session.commit()
    return user


def test_register(testapp):
    request_data = {"username": "user", "password": "abcd1234", "email": "hello"}
    resp = testapp.post(
        "/register", content_type="application/json", data=json.dumps(request_data)
    )
    assert resp.status_code == 200
    assert User.query.count() == 1


def test_login(testapp):
    request_data = {"username": "user", "password": "abcd1234", "email": "hey"}
    resp = testapp.post(
        "/register", content_type="application/json", data=json.dumps(request_data)
    )
    assert resp.status_code == 200
    resp = testapp.post(
        "/auth",
        content_type="application/json",
        data=json.dumps({"username": "user", "password": "abcd1234"}),
    )
    assert resp.status_code == 200
    assert resp.json["user"]["username"] == request_data["username"]


def test_get_users(testapp):
    create_user(testapp)
    create_user(testapp)
    resp = testapp.get("/users")
    assert resp.status_code == 200
    body = resp.json
    assert len(body["users"]) == 2


def test_protected_resource(testapp):
    resp = testapp.get("/test-protected")
    assert resp.status_code == 401
    user = create_user(testapp)
    resp = testapp.post(
        "/auth",
        content_type="application/json",
        data=json.dumps({
            "username": user.username,
            "password": UserFactory.get_password(user),
        }),
    )
    assert resp.status_code == 200
    token = resp.json.get("access_token")
    resp = testapp.get(
        "/test-protected", headers={"Authorization": "JWT {}".format(token)}
    )
    assert resp.status_code == 200


# def test_create_listing(testapp):
#     user = create_user(testapp)
#     resp = testapp.post(
#         "/auth",
#         content_type="application/json",
#         data=json.dumps(
#             {"username": user.username, "password": UserFactory.get_password(user)}
#         ),
#     )
#     assert resp.status_code == 200
#     token = resp.json.get("access_token")
#     request_data = {"title": "nice"}
#     resp = testapp.post(
#         "/users/{}/listings".format(user.id),
#         content_type="application/json",
#         data=json.dumps(request_data),
#         headers={"Authorization": "JWT {}".format(token)},
#     )
#     assert resp.status_code == 200
#     assert resp.json["title"] == "nice"
