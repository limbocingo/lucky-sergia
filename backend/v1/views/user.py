"""
LuckySergia source code user blueprint.

[version: v1]
[author: mrcingo]
"""
import flask
import peewee

from playhouse.shortcuts import model_to_dict

from backend.models import *
from backend.utils.authentication import authenticate

blueprint = flask.Blueprint('users', __name__)


@blueprint.route('/', methods=['POST', 'GET'])
@authenticate
def users():
    if flask.request.method == 'POST':
        content = flask.request.json
        if 'username' not in content or 'password' not in content or 'email' not in content:
            return flask.jsonify({'message': 'Missing argument, password or username.'}), 400

        try:
            user = User(username=content['username'],
                        password=content['password'],
                        email=content['email'],
                        sid=''.join(choices(ascii_letters + digits, k=64)))
            user.save()
        except peewee.IntegrityError:
            return flask.jsonify({'message': 'User already exists.'}), 400

        return flask.jsonify(model_to_dict(user, exclude=[User.password]))

    users = User.select()

    response = []
    for user in users:
        response.append(model_to_dict(user, exclude=[User.password]))

    return flask.jsonify(response), 200


@blueprint.route('/<sid>/', methods=['PATCH', 'GET', 'DELETE'])
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

        data = {}
        for i in content:
            if i not in User._meta.sorted_field_names:
                continue

            data[i] = content[i]

        user_update = User.update(
            data
        ).where(User == user)
        user_update.execute()

        return flask.jsonify(model_to_dict(User.get(User.sid == sid), exclude=[User.password]))

    return flask.jsonify(model_to_dict(user, exclude=[User.password]))


@blueprint.route('/<username>/login/', methods=['POST'])
@authenticate
def login(username):
    try:
        user = User.get(User.username == username)
    except peewee.DoesNotExist:
        return flask.jsonify({'message': 'User does not exist.'}), 404

    content = flask.request.json

    if 'password' not in content:
        return flask.jsonify({'message': 'Missing argument, password.'}), 400

    if content['password'] != user.password:
        return flask.jsonify({'message': 'Wrong password, try again.'}), 400

    if user.logged:
        return flask.jsonify({'message': 'User is already logged in.'})

    user_update = User.update(logged=True).where(User == user)
    user_update.execute()

    return {'sid': user.sid}


@blueprint.route('/<sid>/logout/', methods=['POST'])
@authenticate
def logout(sid):
    try:
        user = User.get(User.sid == sid)
    except peewee.DoesNotExist:
        return flask.jsonify({'message': 'User does not exist.'}), 404

    if not user.logged:
        return flask.jsonify({'message': 'User is not logged in.'}), 400

    user_update = User.update(logged=False).where(User == user)
    user_update.execute()

    return {'message': 'User Log Out successfully.'}
