"""
Logic and view for the LuckySergia games.

[version: v1]
[author: mrcingo]
"""
import flask
import random

from backend.utils.authentication import authenticate


blueprint = flask.Blueprint('games', __name__,)


@blueprint.route('/crash/', methods=['POST'])
@authenticate
def crash():
    if not flask.request.json.get('sid') or not flask.request.json.get('stop'):
        return flask.jsonify({'message': 'You did not passed the `sid` or `stop`.'}), 400

    return flask.jsonify(random.randint(0, 10)) 
