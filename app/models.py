from mongoengine import *
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
#g is global variable set by flaskauth, refers to user`
from datetime import datetime
from app import auth

class User(Document):
    username = StringField(max_length = 256, required = True, primary_key = True)
    password_hash = StringField(max_length = 256, min_length = 256, required = True)
    
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
        s = Serializer(flaskApp.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user
    
    def __repr__(self):
        return '<User %r>' % (self.username)

class Message(Document):
    _id = StringField(primary_key = True)
    create_time = DateTimeField(required = True)
    body = StringField(required = True)
    author = StringField(required = True)
    recipients_list = ListField(StringField(), required = True)
    def __init__(self):
        self.create_time = datetime.utcnow()
    def __repr__(self):
        return '<Author %r, recipient %r>' % (self.author, self.recipients_list)
    
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    auth.g.user = user
    return True

