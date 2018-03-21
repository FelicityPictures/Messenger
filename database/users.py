from . import db
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

    def set_password(self, password):
        self.password_hash = hashpw(password.encode('utf-8'), gensalt())

    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password_hash)
