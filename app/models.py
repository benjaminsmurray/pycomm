from app import flaskdb, flaskAuth, flaskApp
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
#g is global variable set by flaskauth, refers to user`
from flask import g
from datetime import datetime

class User(flaskdb.Document):
    _id = flaskdb.StringField(max_length = 200, required = True, unique = True)
    password_hash = flaskdb.StringField(required = True)
    
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

class Message(flaskdb.Document):
    _id = flaskdb.StringField(primary_key = True)
    send_date = flaskdb.DateTimeField(required = True, default=datetime.now)
    body = flaskdb.StringField(required = True)
    author = flaskdb.StringField(required = True)
    recipient = flaskdb.ListField(required = True)
    def __init__(self, body, author, recipient):
        self.send_date = datetime.utcnow()
        self.body = body
        self.author = author
        self.recipient = recipient
    def __repr__(self):
        return '<Author %r, recipient %r>' % (self.author, self.recipient)
    
@flaskAuth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

