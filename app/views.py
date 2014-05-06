from flask import request, jsonify, url_for, abort, Flask
from app import flaskApp, auth
import app.models as models
from datetime import datetime
from mongoengine.errors import NotUniqueError

@flaskApp.route('/')
@flaskApp.route('/index')
@flaskApp.route('/user', methods = ['GET'])
def index():
    return ("hello")

#register a new user
'''
new_user input json

{'username': 'user1', 'password': 'blah%blah2'}

output:
{'created'}

'''

@flaskApp.route('/user', methods = ['POST'])
def new_user():
    request_json = request.get_json()
    username = request_json['username']
    password = request_json['password']

    if username is None or password is None:
        abort(400) # missing arguments
    '''TODO:
        The lines commented below check to see if the provided username already exists.
        However, using this there is a race condition before the .save a at the end of the function,
        So there is no gurantee a user does not get overwritten. So for now, I won't even pretend
        To prevent user overwrites. Relying on 'unique' constraint set in the model on the 'username' field
    '''
    #if models.User.available_username(username = username) is False:
     #   abort(400) # existing user

    #make the user object. 
    new_user = models.User(username = username)
    new_user.set_password(password)
    #save to db
    try:
        new_user.save()
        return jsonify({ "created":""})
    except NotUniqueError:
        print("not unique")
        abort(400) #existing user   

#send a message
@flaskApp.route('/message', methods = ['POST'])
@auth.login_required
def send_message():
    request_json = request.get_json()
    body = request_json['body']
    recipients = request_json['recipients']

    if recipients is None or body is None:
        abort(400) # missing args
    recipients_tuple = tuple(recipients)

    message = models.Message(text = body, author = auth.user, create_time = datetime.utcnow())

    if recipients_tuple in auth.user.conversations:
        #conversation between recipients already exists
        conversation_id = auth.user.conversations[recipients]
        models.send_message(recipients_tuple, conversation_id, message)
    else:
        models.start_conversation(recipients_tuple, auth.user, message)
        
        #use objectID from map to find conversation ID
        #add message to conversation
    #else
        #create conversation
        #add new message to conversation
        # insert conversation objectID into conversation map for each user in recipients list, including calling user
    return jsonify({"message sent": body})

@flaskApp.route('/token')
@auth.login_required
def get_auth_token():
    token = auth.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })