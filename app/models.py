#!/usr/bin/env python

from datetime import datetime
from flask import current_app
from . import db, ma, bc


class User(db.Model):
    id = db.Column(
        db.BigInteger,
        primary_key=True,
    )
    username = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
    )
    password_hash = db.Column(
        db.String(255),
        nullable=False,
    )
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
    )
    created = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
        index=True,
    )
    admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, **kwargs):
        password = kwargs.pop('password')
        super(User, self).__init__(**kwargs)
        self.password_hash = bc.generate_password_hash(
            password,
            current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


user_schema = UserSchema(exclude=['password_hash'])
users_schema = UserSchema(many=True, exclude=['password_hash'])


# class Listing(db.Model):
#     id = db.Column(
#         db.BigInteger,
#         primary_key=True
#     )
#     user_id = db.Column(
#         db.BigInteger,
#         unique=True,
#         nullable=False,
#     )
#     title = db.Column(
#         db.String(255),
#         nullable=False,
#     )


# class Attribute(db.Model):
#     listing_id = db.Column(
#         db.BigInteger,
#         primary_key=True,
#     )
#     key = db.Column(
#         db.String(30),
#         primary_key=True,
#     )
#     value = db.Column(
#         db.String(),
#         nullable=False,
#     )


# from sqlalchemy.schema import Index
# # secondary btree index on key
# Index('Attribute', Attribute.key)


# class ListingSchema(ma.ModelSchema):
#     class Meta:
#         model = Listing


# listing_schema = ListingSchema()
# listings_schema = ListingSchema(many=True)
