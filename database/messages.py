from . import db
from datetime import datetime

class Messages(db.Model):
    # Message Modal
    id = db.Column(db.Integer, primary_key=True)
    sent_time = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'),
        nullable=False)
    message = db.Column(db.Text, nullable=False)
