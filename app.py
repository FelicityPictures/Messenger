from flask import Flask, render_template, flash, redirect, request, session, url_for, abort
from sqlalchemy_utils import create_database, database_exists
from flask_socketio import SocketIO, send, emit
from database import db, Chats, Users, Messages
import logging
import os

logging.basicConfig(level=logging.WARN)

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
    user = Users("ng","thing")
    user2 = Users("wu","thing")
    chat.users.append(user)
    chat.users.append(user2)
    db.session.add(chat)
    db.session.add(user)
    db.session.commit()
    message = Messages("waassap",user.id,chat.id)
    db.session.add(message)
    db.session.commit()
    # print ("\n" + str(user.id) + "    " + str(chat.id) +"\n")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def cant_access_page(e):
    return render_template('403.html'), 403

@app.route('/')
@app.route('/index')
def index():
    if session.get('logged_in'):
        # print('\n activepeople' + str(active_ids)+ '\n')
        return render_template('index.html', users=Users.query.all(),
        current_user=session['current_user'])
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
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if session.get('logged_in'):
        flash("Already logged in!")

    post_username = str(request.form['username'])
    post_password = str(request.form['password'])

    target_user= Users.query.filter(Users.username == post_username).first()

    if not (target_user and target_user.check_password(post_password)):
        flash('fuck off')
        print('Wrong pass')
    else:
        session['logged_in'] = True
        session['current_user'] = target_user.jasonify()
        print ("\n" + str(session['current_user']) + "\n")
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

@app.route("/chats/<chat_id>")
def chats(chat_id):
    if not session.get('logged_in'):
        flash("Must login")
        return redirect(url_for('login'))
    target_chat = Chats.query.get(chat_id)
    if not target_chat:
        abort(404)
    users_in_chat = target_chat.users_in_chat()
    if session['current_user']['username'] not in users_in_chat:
        abort(403)
    messages = target_chat.messages_in_chat()
    users_in_chat.remove(session['current_user']['username'])
    session['current_chat'] = target_chat.id
    return render_template('index.html', users=Users.query.all(),
    current_user=session['current_user'], chat_id=chat_id, messages=messages,
    users_in_chat=users_in_chat)

@app.route("/new_chat")
def new_chat():
    return render_template('new_chat.html', users=Users.query.all())

@socketio.on('connect')
def connected():
    username = session['current_user']['username']
    print("\n Activate User: " + username)
    emit('active_user', username, broadcast=True) #back to client
    print('\nConnected!\n')

@socketio.on('disconnect')
def disconnected():
    # broadcast to all users that a person is active at this time
    print('\nDisconnected!\n')
    username = session['current_user']['username']
    print("\n Deactivate User: " + username)
    emit('deactive_user', username, broadcast=True) #back to client
    print('\nDisconnected!1\n')

@socketio.on('message')
def my_event(data):
    # message = Messages(data, target_user.id, )
    print("\nMessage: " + data)
    logger.info('Message:' + data + '\n')
    message = Messages(data,session['current_user']['id'],session['current_chat'])
    db.session.add(message)
    db.session.commit()
    emit('new_message', data, broadcast=True) #back to client


if __name__=='__main__':
    app.debug=True
    socketio.run(app, port=8000)
