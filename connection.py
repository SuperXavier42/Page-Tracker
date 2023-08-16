import sqlite3
from flask import g
from urllib import parse
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def get_db():
    con = sqlite3.connect('data.db', check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    db.init_app(app)
    with app.app_context():
       db.create_all()
    return app