#!/usr/bin/env python3

from flask import Flask, render_template, redirect, request, session, url_for
from .users import create_table


app = Flask(__name__)

app.secret_key = "gUG*7BNmM*[*hUd7&y6hb}GlTcub`C"

with app.app_context():
    create_table()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')