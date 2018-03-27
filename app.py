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
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
)

socketio = SocketIO(app)
db.init_app(app)

if not database_exists(db_url):
    create_database(db_url)
db.create_all(app=app)

# One person test case
with app.app_context():
    chat = Chats()
    user = Users("me","thing")
    chat.users.append(user)
    db.session.add(chat)
    db.session.add(user)
    db.session.commit()
    message = Messages("waassap",user.id,chat.id)
    db.session.add(message)
    db.session.commit()
    # print ("\n" + str(user.id) + "    " + str(chat.id) +"\n")

@app.route('/')
@app.route('/home')
def home():
    if session.get('logged_in'):
        return render_template('index.html', users=Users.query.all(),
        current_user=current_user.id)
    else:
        return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if session.get('logged_in'):
        flash("Already logged in!")
        return
    if request.method == 'POST':
        with app.app_context():
            user = Users(request.form['username'], request.form['password'])
            db.session.add(user)
            db.session.commit()
            print('\nRecord was successfully added\n')
        return home()
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if session.get('logged_in'):
        flash("Already logged in!")
        return home()

    post_username = str(request.form['username'])
    post_password = str(request.form['password'])

    target_user= Users.query.filter(Users.username == post_username).first()

    if target_user and target_user.check_password(post_password):
        session['logged_in'] = True
        session['current_user'] = target_user.id
        print ("\n" + str(target_user.chats) + "\n")

    else:
        flash('fuck off')
        print('Wrong pass')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/chats/<chat_id>")
def chats(chat_id):
    if not session.get('logged_in'):
        flash("Must login")
        return home()
    return 'Chat %s' % chat_id

@socketio.on('connected')
def connected():
    # broadcast to all users that a person is active at this time, keep a
    # global
    print('\nConnected!\n')

@socketio.on('disconnected')
def disconnected():
    # broadcast to all users that a person is active at this time
    print('\nDisconnected!\n')

@socketio.on('message')
def my_event(data):
    message = Messages(data, target_user.id, )
    print("\nMessage: " + data)
    logger.info('Message:' + data + '\n')
    emit('new_message', data, broadcast=True) #back to client

if __name__=='__main__':
    app.debug=True
    socketio.run(app, port=8000)
    app.run(host='0.0.0.0', port=8000)
