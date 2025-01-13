from connection import get_db_tuple
from flask import session
from datetime import datetime, timedelta

#this file manages all data for the finished books data base
#all editing is done through these functions

def create_finished_books():
    connection = get_db_tuple()
    sql = connection.cursor()
    sql.execute(
        """create table if not exists finished_books (
        "user_id" Integer,
        "book_name" Text,
        "date_finished" Text
    )"""
    )

def add_book(book_name, date):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    row1 = sql.execute("SELECT * FROM books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name]).fetchall()
    row2 = sql.execute("SELECT * FROM planned_books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name]).fetchall()
    row3 = sql.execute("SELECT * FROM finished_books WHERE (user_id = ? AND  book_name = ?)", [user_id, book_name]).fetchall()
    if(len(row1)>0 or len(row2)>0 or len(row3)>0):
        return "Book already on the list"
    else:
        sql.execute("INSERT into finished_books (user_id, book_name, date_finished) values (?, ?, ?)", [user_id, book_name, date])
        connection.commit()
        return "Book added"
    
def delete_book(book_name):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    sql.execute("DELETE FROM finished_books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name])
    connection.commit()
    return "Book deleted"

def locate_books():
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    result = sql.execute("SELECT book_name, date_finished FROM finished_books WHERE user_id = ?", [user_id]).fetchall()
    return result