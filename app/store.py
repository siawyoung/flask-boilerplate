#!/usr/bin/env python

from flask import jsonify
from .models import User
from .models import user_schema
from . import bc
# from .models import Listing


class UserStore:
    def __init__(self, db):
        self.db = db

    def get_user_by_id(self, id):
        user = User.query.filter(User.id == id).first()
        return user

    def get_all_users(self):
        users = User.query.all()
        return users

    def create_user(self, user):
        self.db.session.add(user)
        self.db.session.commit()

    def registration_check(self, username, email):
        if not username or not email:
            return True
        return (
            User.query.filter(User.username == username or User.email == email).count()
            != 0
        )

    def check_login(self, username, password):
        user = User.query.filter(User.username == username).first()
        does_password_match = bc.check_password_hash(user.password_hash, password)
        if does_password_match:
            return user

    def get_user_by_token_claim(self, token):
        id = token.get('identity')
        return self.get_user_by_id(id)


def auth_response(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user': user_schema.dump(identity),
    })


# class ListingStore:
#     def __init__(self, db):
#         self.db = db

#     def get_listings_by_user_ids(self, user_ids):
#         return Listing.query.filter(Listing.user_id.in_(user_ids))
