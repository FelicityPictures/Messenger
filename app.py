from flask import Flask, render_template
from sqlalchemy_utils import create_database, database_exists
from flask_socketio import SocketIO, send, emit
from database import db, Chats, Persons
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('app')

app = Flask(__name__)

db_url = 'sqlite:///messenger.db'

app.config.update(
    SECRET_KEY='secret!',
    SQLALCHEMY_DATABASE_URI=db_url,
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
)
socketio = SocketIO(app)
db.init_app(app)

if not database_exists(db_url):
    create_database(db_url)
db.create_all(app=app)

with app.app_context():
    chat = Chats()
    db.session.add(chat)
    db.session.commit()

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@socketio.on('connected')
def connected():
    print('Connected!')

@socketio.on('message')
def my_event(data):
    print("Message: " + data)
    logger.info('Message:' + data)

if __name__=='__main__':
    app.debug=True
    socketio.run(app, port=8000)
    # app.run(host='0.0.0.0', port=8000)
