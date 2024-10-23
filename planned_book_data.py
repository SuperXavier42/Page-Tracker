from connection import get_db_tuple
from flask import session
from datetime import datetime, timedelta

def create_planned_books():
    connection = get_db_tuple()
    sql = connection.cursor()
    sql.execute(
        """create table if not exists planned_books (
        "user_id" Integer,
        "book_name" Text
    )"""
    )

def add_book(book_name):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    rows = sql.execute("SELECT * FROM planned_books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name]).fetchall()
    if(len(rows)>0):
        return "Book already on the list"
    else:
        sql.execute("INSERT into planned_books (user_id, book_name) values (?, ?)", [user_id, book_name])
        connection.commit()
        return "Tracking book"
    
def start_book(book_name, page_total, days_left):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    rows = sql.execute("SELECT * FROM books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name]).fetchall()
    if(len(rows)>0):
        return "Book already being tracked"
    else:
        date=datetime.now()
        target_date=date + timedelta(days=int(days_left))
        target_date = target_date.replace(hour=0, minute=0, second=0)
        sql.execute("INSERT into books (user_id, book_name, page_total, days_left, target_date) values (?, ?, ?, ?, ?)", [user_id, book_name, page_total, days_left, target_date])
        sql.execute("DELETE FROM planned_books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name])
        connection.commit()
        return "Tracking book"
    
def delete_book(book_name):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    sql.execute("DELETE FROM planned_books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name])
    connection.commit()
    return "Book deleted"

def locate_books():
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    result = sql.execute("SELECT book_name FROM planned_books WHERE user_id = ?", [user_id]).fetchall()
    return result