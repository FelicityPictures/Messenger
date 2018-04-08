from . import db, dump_datetime
from datetime import datetime

class Messages(db.Model):
    # Message Modal
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    sent_time = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'),
        nullable=False)

    def __init__(self, message, sender_id, chat_id):
        self.message = message
        self.sent_time = datetime.utcnow()
        self.sender_id = sender_id
        self.chat_id = chat_id

    def get_sender_username(self):
        return Users.query.get(self.sender_id).username

    def jasonify(self):
        return{
            'id'        : self.id,
            'message'   : self.message,
            'sent_time' : self.sent_time,
            'sender_id' : self.sender_id,
            'sender_username' : self.sender_username,
            'chat_id'   : self.chat_id
        }
