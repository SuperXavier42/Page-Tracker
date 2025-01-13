from connection import get_db_tuple
from flask import session
from datetime import datetime, timedelta

#this file manages all data for the planned books data base
#all editing is done through these functions

def create_planned_books():
    connection = get_db_tuple()
    sql = connection.cursor()
    sql.execute(
        """create table if not exists planned_books (
        "user_id" Integer,
        "book_name" Text,
        "page_count" Integer
    )"""
    )

#this function adds books to planned database
def add_book(book_name):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    #checks if another instance of the book exists
    row1 = sql.execute("SELECT * FROM books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name]).fetchall()
    row2 = sql.execute("SELECT * FROM planned_books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name]).fetchall()
    row3 = sql.execute("SELECT * FROM finished_books WHERE (user_id = ? AND  book_name = ?)", [user_id, book_name]).fetchall()
    if(len(row1)>0 or len(row2)>0 or len(row3)>0):
        return "Book already on the list"
    else:
        sql.execute("INSERT into planned_books (user_id, book_name, page_count) values (?, ?, ?)", [user_id, book_name, 0])
        connection.commit()
        return "Tracking book"

#function moves book from planned database to current database
def start_book(book_name, page_total, days_left):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    rows = sql.execute("SELECT * FROM books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name]).fetchall()
    if(len(rows)>0):
        return "Book already being tracked"
    else:
        #creates the final date, so it can track days remaining
        date=datetime.now()
        target_date=date + timedelta(days=int(days_left)+1)
        target_date = target_date.replace(hour=0, minute=0, second=0)
        sql.execute("INSERT into books (user_id, book_name, page_total, days_left, target_date) values (?, ?, ?, ?, ?)", [user_id, book_name, page_total, days_left, target_date])
        sql.execute("DELETE FROM planned_books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name])
        connection.commit()
        return "Tracking book"

#takes book name and user id and deletes the corresponding book from the planned database
def delete_book(book_name):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    sql.execute("DELETE FROM planned_books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name])
    connection.commit()
    return "Book deleted"

#requests all books to display on the plan to read html page
def locate_books():
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    result = sql.execute("SELECT book_name, page_count FROM planned_books WHERE user_id = ?", [user_id]).fetchall()
    return result