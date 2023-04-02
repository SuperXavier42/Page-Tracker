#!/usr/bin/env python3

import requests
import secrets
from flask import Flask, render_template, redirect, request, session, url_for
from .users import create_table, check_account, create_account
from .auth import auth_bp

def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]

code_verifier = code_challenge = get_new_code_verifier()

app = Flask(__name__)

app.secret_key = "gUG*7BNmM*[*hUd7&y6hb}GlTcub`C"

app.register_blueprint(auth_bp)

url="https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id=79a3722f91d0b23adeadcd21f4b5896e&code_challenge="+str(code_challenge)

MAL = requests.get(url)

with app.app_context():
    create_table()

@app.route('/')
def home():
    if session.get("logged_in"): 
        user_id = session.get('user_id')
        return render_template('home.html')
    else:
        return redirect(url_for('auth.login_page'))
        
@app.route('/watch')
def watch():
    return render_template('watch.html')        
    
