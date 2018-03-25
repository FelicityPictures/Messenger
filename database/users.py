from . import db, dump_datetime
from datetime import datetime
from bcrypt import checkpw, hashpw, gensalt

class Users(db.Model):
    # user Modal
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    last_active = db.Column(db.DateTime, nullable=False,
            default=datetime.utcnow)
    messages = db.relationship('Messages', backref='users', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = hashpw(password.encode('utf-8'), gensalt())
        last_active = datetime.utcnow()

    def set_password(self, password):
        self.password_hash = hashpw(password.encode('utf-8'), gensalt())

    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password_hash)

    def jasonify(self):
        #Return object data in easily serializeable format
        return {
           'id'         : self.id,
           'last_active': dump_datetime(self.last_active),
           'username'   : self.username,
           'messages'   : [m.lean() for m in self.messages]
        }

    def jasonify_lean(self):
        return{
            'id'        : self.id,
            'username'  : self.username
        }
