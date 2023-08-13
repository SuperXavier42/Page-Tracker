import sqlite3
from sqlite3 import Error
from flask import g

db_file = 'D:\VSCode\Website\data.db'

def get_db():
    connection = g.get('db', 'null')
    if connection == 'null':
        g.db = sqlite3.connect(db_file)
        g.db.row_factory = sqlite3.Row
        return g.db
    else:
        return connection