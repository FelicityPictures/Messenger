from . import db
from datetime import datetime

class Users(db.Model):
    # user Modal
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    last_active = db.Column(db.DateTime, nullable=False,
            default=datetime.utcnow)
    messages = db.relationship('Messages', backref='users', lazy=True)

    # def seralize_all(self):
