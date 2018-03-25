from flask import Flask, render_template, flash, redirect, request, session, abort
from sqlalchemy_utils import create_database, database_exists
from flask_socketio import SocketIO, send, emit
from database import db, Chats, Users, Messages
import logging
import os

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('app')

app = Flask(__name__)

db_url = 'sqlite:///:memory:'

app.config.update(
    SECRET_KEY='secret!',
    SQLALCHEMY_DATABASE_URI=db_url,
    # the app istself is a multithreaded, so it keeps a pool of db session.
    # sqla makes sessions a global context and stored in db
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
)
socketio = SocketIO(app)
db.init_app(app)

if not database_exists(db_url):
    create_database(db_url)
db.create_all(app=app)

# One person test case
with app.app_context():
    user = Users("me","thing")
    print('first guy!')
    db.session.add(user)
    db.session.commit()

@app.route('/')
@app.route('/home')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html', users=Users.query.all(),
        user=sessions['username'])

@app.route('/login', methods=['GET','POST'])
def login():
    if session.get('logged_in'):
        flash("Already logged in!")

    post_username = str(request.form['username'])
    post_password = str(request.form['password'])

    target_user= Users.query.filter(Users.username == post_username).first()

    if target_user and target_user.check_password(post_password):
        session['logged_in'] = True
        session['username'] = post_username
    else:
        flash('fuck off')
        print('Wrong pass')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/register', methods=['POST', 'GET'])
def register():
    if session.get('logged_in'):
        flash("Already logged in!")
        return home()
    if request.method == 'POST':
        with app.app_context():
            user = Users(request.form['username'], request.form['password'])
            db.session.add(user)
            db.session.commit()
            print('\nRecord was successfully added\n')
        return home()
    return render_template('register.html')

@socketio.on('connected')
def connected():
    print('Connected!')

@socketio.on('message')
def my_event(data):
    print("\nMessage: " + data)
    logger.info('Message:' + data + '\n')
    emit('new_message', data, broadcast=True) #back to client

if __name__=='__main__':
    app.debug=True
    socketio.run(app, port=8000)
    app.run(host='0.0.0.0', port=8000)
