#!/usr/bin/env python

from collections import defaultdict

from flask import current_app as app
from flask import jsonify
from flask import request
from flask_jwt import jwt_required, current_identity

from .models import User
from .models import db
from .models import user_schema
from .models import users_schema
from .store import UserStore
# from .models import Listing
# from .store import ListingStore
# from .models import listing_schema
# from .models import listings_schema


user_store = UserStore(db)
# listing_store = ListingStore(db)


def join(A, B, identifier, A_join_key, B_join_key):
    """Join B to A through join_key"""
    B_dict = defaultdict(list)
    for i in B:
        B_dict[i[B_join_key]].append(i)
    for i in A:
        i[identifier] = B_dict[i[A_join_key]]


@app.route("/users", methods=["GET"])
def get_users():
    users = user_store.get_all_users()
    # listings = listing_store.get_listings_by_user_ids([x.id for x in users])
    # serialized_listings = listings_schema.dump(listings)
    serialized_users = users_schema.dump(users)
    # join(serialized_users, serialized_listings, "listings", "id", "user_id")
    return jsonify({"users": serialized_users})


# @app.route("/users/<user_id>/listings", methods=["POST"])
# @jwt_required()
# def create_listing(user_id):
#     if str(user_id) != str(current_identity.id):
#         return jsonify({"Error": "User ID not valid"}), 403
#     body = request.json
#     title = body.get("title")
#     listing = Listing(title=title, user_id=user_id)
#     db.session.add(listing)
#     db.session.commit()
#     return listing_schema.jsonify(listing)


@app.route("/register", methods=["POST"])
def register():
    user = request.json
    username = user.get("username")
    password = user.get("password")
    email = user.get("email")
    is_taken = user_store.registration_check(username, email)
    if is_taken:
        return jsonify({"Error": "Already taken"}), 400
    user = User(username=username, password=password, email=email)
    user_store.create_user(user)
    u = user_schema.jsonify(user)
    return u


@app.route("/test-protected", methods=["GET"])
@jwt_required()
def test_protected():
    return jsonify({"test": "hey"}), 200
