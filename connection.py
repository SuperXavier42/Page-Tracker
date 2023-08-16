import sqlite3
from sqlite3 import Error
from flask import Flask

def get_db():
    con = sqlite3.connect('data.db', check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con