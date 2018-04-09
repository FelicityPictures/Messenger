from . import db, dump_datetime
from datetime import datetime
from bcrypt import checkpw, hashpw, gensalt

class Users(db.Model):
    # user Modal
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False, unique=True)
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

    # returns a bool if the chat exits given a person_id
    def check_private_chat_exits(self, id):
        private_chats = [chat.users_id_in_chat() for chat in self.chats if len(chat.users) == 2]
        print ("private chats: " + str(private_chats))
        for chat in private_chats:
            for chat_id, users in chat.items():
                print("pairing chat_id:" + str(id) + "user_id" + str(users))
                if id in users:
                    return (True, chat_id)
        return (False, 0)

    def jasonify(self):
        #Return object data in easily serializeable format
        return {
           'id'         : self.id,
           'last_active': dump_datetime(self.last_active),
           'username'   : self.username,
           'chats'      : [chat.id for chat in self.chats],
           'chats_user' : [chat.users_in_chat() for chat in self.chats]
           }
