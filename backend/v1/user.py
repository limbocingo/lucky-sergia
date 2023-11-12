"""
LuckySergia source code user blueprint.

[version: v1]
[author: mrcingo]
"""
import flask
import peewee

from backend.models import *
from backend.utils.authentication import authenticate

userbp = flask.Blueprint('user',
                         __name__,
                         url_prefix='/api/v1/users'
                         )


@userbp.route('/', methods=['POST', 'GET'])
@authenticate
def users():
    if flask.request.method == 'POST':
        content = flask.request.json
        if 'username' not in content or 'password' not in content:
            return flask.jsonify({'message': 'Missing argument, password or username.'}), 400

        try:
            user = User(username=content['username'],
                        password=content['password'])
            user.save()
        except peewee.IntegrityError:
            return flask.jsonify({'message': 'User already exists.'}), 400

        return flask.jsonify({'id': user.get_id(),
                              'username': user.username,
                              'email': user.email,
                              'password': user.password,
                              'balance': user.balance,
                              'sid': user.sid}
                             ), 200

    users = User.select()

    response = []
    for user in users:
        response.append({'id': user.get_id(),
                         'username': user.username,
                         'email': user.email,
                         'balance': user.balance,
                         'sid': user.sid})

    return flask.jsonify(response), 200


@userbp.route('/search/<username>', methods=['GET'])
@authenticate
def search_by_name(username):
    try:
        user = User.get(User.username == username)
    except peewee.DoesNotExist:
        return flask.jsonify({'message': 'User does not exist.'}), 404

    return flask.jsonify({'id': user.id,
                          'username': user.username,
                          'balance': user.balance,
                          'email': user.email,
                          'sid': user.sid}
                         )


@userbp.route('/<sid>/', methods=['PATCH', 'GET', 'DELETE'])
@authenticate
def user(sid):
    try:
        user = User.get(User.sid == sid)
    except peewee.DoesNotExist:
        return flask.jsonify({'message': 'User does not exist.'}), 404

    if flask.request.method == 'DELETE':
        user.delete_instance()

        return flask.jsonify({'message': 'User removed from DB.'})

    if flask.request.method == 'PATCH':
        content = flask.request.json

        username = content.get('username')
        password = content.get('password')
        email = content.get('email')
        balance = content.get('balance')

        user_update = User.update(
            username=username if username else user.username,
            password=password if password else user.password,
            email=email if email else user.email,
            balance=balance if balance else user.balance,
        ).where(User == user)
        user_update.execute()

        return flask.jsonify({'id': user.id,
                              'username': user.username,
                              'balance': user.balance,
                              'email': user.email,
                              'sid': user.sid})

    return flask.jsonify({'id': user.id,
                          'username': user.username,
                          'balance': user.balance,
                          'email': user.email,
                          'sid': user.sid})


@userbp.route('/<id>/password/', methods=['POST'])
@authenticate
def check_password(id):
    try:
        user = User.get(User.id == id)
    except peewee.DoesNotExist:
        return flask.jsonify({'message': 'User does not exist.'}), 404

    content = flask.request.json

    if 'password' not in content:
        return flask.jsonify({'message': 'Missing argument, password.'}), 400

    return {'valid': content['password'] == user.password}
