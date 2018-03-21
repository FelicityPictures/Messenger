from . import db

persons_to_chat = db.Table('persons_to_chat', db.metadata,
    db.Column('person_id', db.Integer, db.ForeignKey('persons.id'), primary_key=True),
    db.Column('chat_id', db.Integer, db.ForeignKey('chats.id'), primary_key=True)
)

class Chats(db.Model):
    # Chat Modal
    id = db.Column(db.Integer, primary_key=True)
    # Persons load after the chat, so query the chat with people in it.
    persons = db.relationship('Persons', secondary=persons_to_chat, lazy='subquery',
        backref=db.backref('chats', lazy=True))
    #one-to-many rel with messages 
    messages = db.relationship('Messages', backref='chats', lazy=True)
