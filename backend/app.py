"""
LuckySergia main App.

[author: mrcingo]
"""
import flask
import sys

from backend.models import *
from backend.utils.authentication import authenticate
from backend.utils.versioning import BlueprintVersioning

app = flask.Flask(__name__)
versioning = BlueprintVersioning(app)
versioning.register()


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.errorhandler(404)
def bad_method(e):
    return flask.jsonify({'message': 'Unknown path.'}), 404


@app.errorhandler(405)
def bad_method(e):
    return flask.jsonify({'message': 'Method not suported.'}), 405


@app.errorhandler(505)
def internal_error(e):
    return flask.jsonify({'message': 'Internal error.'}), 505


@app.route('/api/')
@authenticate
def api():
    return flask.jsonify({'message': 'Lucky Sergia'})
