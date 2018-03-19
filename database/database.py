from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#helper many-to-many relationship persons and chat
chats = db.Table('chats', db.metadata,
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'), primary_key=True),
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True)
)

class Person(db.Model):
    # Person Modal
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    last_active = db.Column(db.DateTime, nullable=False,
            default=datetime.utcnow)
    # Chat loads after loading a person, but using a separate query.
    chats = db.relationship('Chats', secondary=chats, lazy='subquery',
        backref=db.backref('persons', lazy=True))

class Chat(db.Model):
    # Chat Modal
    id = db.Column(db.Integer, primary_key=True)
