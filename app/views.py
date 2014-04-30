from flask import request, jsonify, g, url_for, abort, Flask
from app import flaskApp, auth

@flaskApp.route('/')
@flaskApp.route('/index')
@flaskApp.route('/user', methods = ['GET'])
def index():
    return ("hello")

#register a new user
@flaskApp.route('/user', methods = ['POST'])
def new_user():
    username = request.get_json('username')
    #TODO: assert username does not contain '@'
    password = request.get_json('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if models.User.available_username(username = username) is False:
        abort(400) # existing user
    #make the user object. 
    new_user = models.User(username = username, password_hash = user.hash_password(password))
    #save to db
    new_user.save()
    return jsonify({ "new user created":username})

#send a message
@flaskApp.route('/message', methods = ['POST'])
@auth.login_required
def send_message():
    body = request.get_json('body')
    recipients = request.get_json('recipients')
    #recipient list comes in as a string, a list of usernames separated by '@'
    recipient_list = recipients.split("@")
    author = auth.g.user
    print(author)
    if recipient is None or body is None:
        abort(400) # missing args
    message = models.Message(body = body, author = author, recipients = recipients_list)
    message.save()
    return jsonify({"message sent": body})

@flaskApp.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })