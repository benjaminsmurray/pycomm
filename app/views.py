from app import flaskApp, flaskAuth, flaskdb, models
from flask import request, jsonify, g, url_for, abort, Flask

@flaskApp.route('/')
@flaskApp.route('/index')
@flaskApp.route('/user', methods = ['GET'])
def index():
    return ("hello")

#register a new user
@flaskApp.route('/user', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if models.User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = models.User(username = username)
    user.hash_password(password)
    flaskdb.session.add(user)
    flaskdb.session.commit()
    return jsonify({ "new user created":username})

#send a message
@flaskApp.route('/message', methods = ['POST'])
@flaskAuth.login_required
def send_message():
    body = request.json.get('body')
    recipient = request.json.get('recipient')
    author = g.user
    print(author)
    if recipient is None or body is None:
        abort(400) # missing args
    message = models.Message(body = body, author = author, recipient = recipient)
    flaskdb.session.add(message)
    flaskdb.session.commit()
    return jsonify({"message sent":body})

@flaskApp.route('/token')
@flaskAuth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })