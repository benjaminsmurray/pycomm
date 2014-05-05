from flask import request, jsonify, url_for, abort, Flask
from app import flaskApp, auth, models
from datetime import datetime

@flaskApp.route('/')
@flaskApp.route('/index')
@flaskApp.route('/user', methods = ['GET'])
def index():
    return ("hello")

#register a new user
@flaskApp.route('/user', methods = ['POST'])
def new_user():
    request_json = request.get_json()
    username = request_json['username']
    #TODO: assert username does not contain '%'
    password = request_json['password']
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
    request_json = request.get_json()
    body = request_json['body']
    recipients = request_json['recipients']
    if recipients is None or body is None:
        abort(400) # missing args
    #recipient list comes in as a string, a list of usernames separated by '%'
    recipient_list = recipients.split("%")
    #if auth.user.conversations.contais(recipients_list)    
        #use objectID from map to find conversation ID
        #add message to conversation
    #else
        #create conversation
        #add new message to conversation
        # insert conversation objectID into conversation map for each user in recipients list, including calling user
    author = auth.user
    message = models.Message()
    message.body = body
    message.author = author.username
    message.recipients = recipient_list
    message.create_time = datetime.utcnow()
    message.save()
    return jsonify({"message sent": body})

@flaskApp.route('/token')
@auth.login_required
def get_auth_token():
    token = auth.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })