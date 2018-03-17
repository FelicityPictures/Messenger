from flask import Flask, render_template, redirect, request, session, url_fo
import json

app = flask(_name_)

@app.route('/', methods=["POST"])
@app.route('/home', methods=["POST"])
def home():
        return render_template('index.html', user=session['username'])

@app.route('/login', methods=["GET","POST"])
@app.route('/login/<error>', methods=['GET','POST'])
def login(error=None):
    return render_template('login.html'), 401