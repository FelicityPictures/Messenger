from flask import Flask, render_template, flash, redirect, request, session, url_for, abort
from sqlalchemy_utils import create_database, database_exists
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from database import db, Chats, Users, Messages, dump_datetime
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.WARN)

logger = logging.getLogger('app')

app = Flask(__name__)

db_url = 'sqlite:///:memory:'

all_active_users = {}

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
    user3 = Users("chou","thing")
    user4 = Users("xu","thing")
    chat.users.append(user)
    chat.users.append(user2)
    chat.users.append(user3)
    chat.users.append(user4)
    db.session.add(chat)
    db.session.add(user)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.commit()
    message = Messages("waassap",user.id,chat.id)
    db.session.add(message)
    db.session.commit()

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
        return redirect(url_for('chats', chat_id=1))
    else:
        return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if session.get('logged_in'):
        flash("Already logged in!")
        return
    if request.method == 'POST':
        user = Users(request.form['username'], request.form['password'])
        db.session.add(user)
        global_chat = Chats.query.get(1)
        global_chat.users.append(user)
        try:
            db.session.commit()
        except:
            flash('A user with that username already exists')
            return render_template('register.html')
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
        flash('Login failed')
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
def chats(chat_id, new_chat=False):
    if not session.get('logged_in'):
        flash("Must login")
        return redirect(url_for('login'))
    target_chat = Chats.query.get(chat_id)
    if not target_chat:
        abort(404)
    users_in_chat = target_chat.users_in_chat()
    if session['current_user']['username'] not in users_in_chat:
        abort(403)
    session['current_user'] = Users.query.get(session['current_user']['id']).jasonify()
    messages = target_chat.messages_in_chat()
    users_in_chat.remove(session['current_user']['username'])
    session['current_chat'] = target_chat.id
    all_but_self = Users.query.all()
    all_but_self.remove(Users.query.get(session['current_user']['id']))
    return render_template('chat.html', users=all_but_self, current_user=session['current_user'],
    chat_id=chat_id, messages=messages, users_in_chat=users_in_chat, new_chat=False)

@app.route("/new_chat", methods=['GET','POST'])
def new_chat():
    if request.method == 'GET':
    # everyone but yourself! Unless you wanna talk to yourself. Weirdo
        users = Users.query.filter(Users.id != session['current_user']['id']).all()
        return render_template('new_chat.html', users=users,current_user=session['current_user'])
    # the request form comes in a string, so this will typecast value to int
    people = [int(i) for i in request.form.getlist("people")]
    print("\nPeople:" + str(people) + "\n")
    current_user = Users.query.get(session['current_user']['id'])
    if len(people) == 1:
        exist = current_user.check_private_chat_exits(people[0])
        if exist[0]:
            print("\nIT EXITS\n")
            return(redirect(url_for('chats', chat_id=exist[1])))
    print("\nmaking new\n")
    new_chat = Chats()
    new_chat.users.append(current_user)
    for person in people:
        user = Users.query.get(person)
        new_chat.users.append(user)
    db.session.add(new_chat)
    db.session.commit()
    session['current_user'] = Users.query.get(session['current_user']['id']).jasonify()
    print("\nmade new\n")
    return(redirect(url_for('chats', chat_id=new_chat.id)))

# ===============================================
# Socket Events
# ===============================================

@socketio.on('connect')
def connected():
    user = Users.query.get(session['current_user']['id'])
    user.last_active = datetime.utcnow()
    db.session.commit()
    username = session['current_user']['username']
    print("\n Activate User: " + username)
    sid = request.sid
    global all_active_users
    all_active_users[username] = sid
    emit('active_user', (username, sid, all_active_users), broadcast=True) #back to client
    print('\n'+str(all_active_users)+'\n')
    print('\nConnected!\n')

@socketio.on('join')
def join(data):
    print('joined room')
    join_room(data)

@socketio.on('disconnect')
def disconnected():
    # broadcast to all users that a person is active at this time
    print('\nDisconnected!\n')
    username = session['current_user']['username']
    print("\nDeactivate User: " + username)
    emit('deactive_user', username, broadcast=True) #back to client
    print('\nDisconnected!\n')

@socketio.on('leave')
def leave(data):
    print('left room')
    leave_room(data)

@socketio.on('message')
def my_event(data, chat_id):
    print("\nMessage: " + data)
    logger.info('Message:' + data + '\n')
    message = Messages(data,session['current_user']['id'],session['current_chat'])
    db.session.add(message)
    db.session.commit()
    username = session['current_user']['username']
    display = False
    if username in Chats.query.get(chat_id).users_in_chat():
        display = True
    emit('new_message', (data, chat_id, username, display), room=chat_id) #back to client

@socketio.on('add_chat_to_list')
def add_chat_to_list(data):
    pass
    # target_chat = Chats.query.get(data)
    # these_users = target_chat.users_in_chat()
    # print("\nthese:" + these_users)
    # users.remove(session['current_user'])
    # for username in all_active_users.keys():
    #     if username in these_users:
    #         emit('add_chat_to_list', (data, these_users), room=user[username])

if __name__=='__main__':
    app.debug=True
    socketio.run(app, port=8000)
