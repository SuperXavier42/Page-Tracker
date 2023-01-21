from flask import Blueprint, redirect, render_template, session, request, url_for

from .users import create_account, check_account

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login_page'))

@auth_bp.route('/login', methods=['GET', 'POST'])
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

@auth_bp.route('/signup', methods=['GET', 'POST'])
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