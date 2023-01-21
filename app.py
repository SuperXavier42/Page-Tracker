#!/usr/bin/env python3

from flask import Flask, render_template, redirect, request, session, url_for
from .users import create_table, check_account, create_account


app = Flask(__name__)

app.secret_key = "gUG*7BNmM*[*hUd7&y6hb}GlTcub`C"

with app.app_context():
    create_table()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    notif=""
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        current_id=check_account(username, password)
        if not username or not password:
            notif="Fill out all boxes"
        elif current_id:
            session['logged_in']=True
            session['user_id']=current_id
            return redirect(url_for('home'))
        else:
            notif="Wrong username/password"
    if session.get('logged_in')==True:
        return redirect(url_for('home'))
    else:
        return render_template('login.html', error=notif)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    notif=""
    if request.method=='GET':
        return redirect(url_for('login_page'))
    else:
        username=request.form['username']
        password=request.form['password']
        confirm_pass=request.form['confirm-password']
        if not username or not password:
            notif="Fill out all boxes"
        elif password!=confirm_pass:
            notif="Passwords don't match"
        else:
            notif=create_account(username, password)
    return render_template('login.html', error=notif)
        
        
    
