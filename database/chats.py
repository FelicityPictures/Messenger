from . import db

users_to_chat = db.Table('users_to_chat', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('chat_id', db.Integer, db.ForeignKey('chats.id'), primary_key=True)
)

class Chats(db.Model):
    # Chat Modal
    id = db.Column(db.Integer, primary_key=True)
    # users load after the chat, so query the chat with people in it.
    users = db.relationship('Users', secondary=users_to_chat, lazy='subquery',
        backref=db.backref('chats', lazy=True))
    #one-to-many rel with messages
    messages = db.relationship('Messages', backref='chats', lazy=True)

    def users_in_chat(self):
        return [user.username for user in self.users]

    def users_id_in_chat(self):
        return {self.id : [user.id for user in self.users]}

    def messages_in_chat(self):
        return [m.jasonify() for m in self.messages]
