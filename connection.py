import sqlite3
from flask import Flask

def get_db():
    con = sqlite3.connect('data.db', check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def get_db_tuple():
    con = sqlite3.connect('data.db', check_same_thread=False)
    return con