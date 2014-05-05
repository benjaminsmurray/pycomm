from mongoengine import *
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
#g is global variable set by flaskauth, refers to user`
from datetime import datetime
from app import auth, flaskApp

class User(Document):
    username = StringField(max_length = 256, required = True, primary_key = True)
    password_hash = StringField(max_length = 256, min_length = 256, required = True)
    #maps list of recipients to an objectid of the conversation between those recipients
    conversations = MapField(field = ObjectIdField())
    def available_username(username):
        return objects.findOne(username = username) is None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(flaskApp.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        serialized = Serializer(flaskApp.config['SECRET_KEY'])
        try:
            data = serialized.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = objects.first(username=data['id'])
        return user
    
    def __repr__(self):
        return '<User %r>' % (self.username)


class Message(EmbeddedDocument):
    create_time = DateTimeField(required = True)
    text = StringField()
    attachment = GenericReferenceField()
    author = StringField(required = True)
    def __repr__(self):
        return '<Author %r, recipients %r, text %r>' % (self.author, self.recipients, self.text)

class Conversation(Document):
    #'recipients' shouldnt be needed. can get recipient list from map of conversations in each user.
    recipients = ListField(StringField(), required = True)
    messages = ListField(EmbeddedDocumentField(Message))
    def __repr__(self):
        return '<recipients %r>' % (self.recipients)

        
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.objects(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    auth.user = user
    return True

