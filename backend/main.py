import flask
from models import *

app = flask.Flask(__name__)

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response


@app.route('/api/')
def api():
    return flask.jsonify({'message': 'Lucky Sergia'})


@app.route('/api/users/', methods=['POST', 'GET'])
def users():
    if flask.request.method == 'POST':
        content = flask.request.json
        if 'username' not in content or 'password' not in content:
            return flask.jsonify({'message': 'Missing argument, password or username.'}), 400

        user = User(username=content['username'], password=content['password'])   
        user.save()

        return flask.jsonify({'id': user.get_id(), 'username': user.username, 'password': user.password}), 200

    users = User.select()    
    
    response = []
    for user in users:
        response.append({
            'username': user.username,
            'password': user.password,
            'balance': user.balance
        })

    return flask.jsonify(response), 200


if __name__ == '__main__':
    with db:
        db.create_tables([User])

    app.run()
