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
        try:
            user = User.get(User.sid == flask.request.headers.get('Authorization'))
        except peewee.DoesNotExist:
            return flask.jsonify({'message': 'You are not authorized.'}), 401
        
        if user.administrator == False:
            return flask.jsonify({'message': 'You are not authorized.'}), 401

        response =  func(*args, **kwargs)
        response.headers['Access-Control-Allow-Origin'] = '*'

        return response
    return wrapper
