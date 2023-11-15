"""
Logic and view for the LuckySergia games.

[version: v1]
[author: mrcingo]
"""
import random

import flask
import peewee

from backend.models import User
from backend.utils.authentication import authenticate

blueprint = flask.Blueprint('games', __name__,)


def game(user, bet, multiplier):
    if bet > user.balance:
        return flask.jsonify({'message': 'You can not afford that'})

    profit = 0 if not multiplier else bet * multiplier

    user_update = User.update(
        balance = (user.balance - bet) + (profit)
    ).where(User == user)
    user_update.execute()

    if not multiplier:
        return flask.jsonify({'state': False, 'balance': User.get(User.sid == user.sid).balance})
    
    return flask.jsonify({'state': True, 'profit': profit, 'balance': User.get(User.sid == user.sid).balance})

@blueprint.route('/crash/', methods=['POST'])
@authenticate
def crash():
    if not flask.request.json.get('sid') or\
       not flask.request.json.get('multiplier') or\
       not flask.request.json.get('bet'):
        return flask.jsonify({'message': 'You did not passed the `sid`, `multiplier` or `bet` argument.'}), 400

    if not isinstance(flask.request.json.get('bet'), int) or not isinstance(flask.request.json.get('multiplier'), int):
        return flask.jsonify({'message': 'Ets gilipollas.'}), 400

    if flask.request.json.get('bet') < 5:
        return flask.jsonify({'message': 'Bet cannot be less than 5 coins.'})

    if flask.request.json.get('multipler') > 5:
        return flask.jsonify({'message': 'Multiplier is bigger than 5.'})

    try:
        user = User.get(User.sid == flask.request.json.get('sid'))
    except peewee.DoesNotExist:
        return flask.jsonify({'message': 'User does not exist.'}), 404

    bet = int(flask.request.json.get('bet'))
    multiplier = float(flask.request.json.get('multiplier'))
    result = round(random.uniform(0.0, 5.0), 2)

    state = result >= multiplier

    _game = game(user, bet, multiplier if state else 0).json
    _game["result"] = result
 
    return _game


@blueprint.route('/coin/', methods=['POST'])
@authenticate
def coin():
    if not flask.request.json.get('sid') or\
       flask.request.json.get('choice') not in [0, 1] or\
       not flask.request.json.get('bet'):
        return flask.jsonify({'message': 'You did not passed the `sid`, `choice` or `bet` argument.'}), 400

    if not isinstance(flask.request.json.get('bet'), int) or not isinstance(flask.request.json.get('choice'), int):
        return flask.jsonify({'message': 'Ets gilipollas.'}), 400

    if flask.request.json.get('bet') < 5:
        return flask.jsonify({'message': 'Bet cannot be less than 5 coins.'})

    try:
        user = User.get(User.sid == flask.request.json.get('sid'))
    except peewee.DoesNotExist:
        return flask.jsonify({'message': 'User does not exist.'}), 404

    result = random.randint(0, 1)
    bet = int(flask.request.json.get('bet'))
    choice = flask.request.json.get('choice')

    _game = game(user, bet, 2 if choice == result else 0)

    return _game


@blueprint.route('/dice/', methods=['POST'])
@authenticate
def dice():
    if not flask.request.json.get('sid') or\
       not flask.request.json.get('choice') or\
       not flask.request.json.get('bet'):
        return flask.jsonify({'message': 'You did not passed the `sid`, `choice` or `bet` argument.'}), 400

    if not isinstance(flask.request.json.get('bet'), int) or not isinstance(flask.request.json.get('choice'), int):
        return flask.jsonify({'message': 'Ets gilipollas.'}), 400

    if flask.request.json.get('bet') < 5:
        return flask.jsonify({'message': 'Bet cannot be less than 5 coins.'})

    try:
        user = User.get(User.sid == flask.request.json.get('sid'))
    except peewee.DoesNotExist:
        return flask.jsonify({'message': 'User does not exist.'}), 404

    result = random.randint(1, 6)
    bet = int(flask.request.json.get('bet'))
    choice = flask.request.json.get('choice')

    _game = game(user, bet, 3 if choice == result else 0)
    _game["result"] = result

    return _game
