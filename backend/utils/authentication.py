"""
Utilities for LuckySergia.

[author: mrcingo]
"""
import flask
import peewee
from functools import wraps

from backend.models import *


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        try:
            user = User.get(User.sid == flask.request.headers.get('Authorization'))

            if user.administrator == False:
                response = flask.jsonify({'message': 'You are not authorized.'}), 401
        except peewee.DoesNotExist:
            response = flask.jsonify({'message': 'You are not authorized.'}), 401

        response[0].headers['Access-Control-Allow-Origin'] = '*'
        
        return response
    return wrapper
