from flask import session
from connection import get_db_tuple

def create_books():
    connection = get_db_tuple()
    sql = connection.cursor()
    sql.execute(
        """create table if not exists books (
        "user_id" Integer,
        "book_name" Text,
        "page_total" Integer,
        "days_left" Double
    )"""
    )

def add_book(book_name, page_total, days_left):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    result = sql.execute("SELECT * FROM books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name])
    rows = result.fetchall()
    if(len(rows)>0):
        return "Book already being tracked"
    else:
        sql.execute("INSERT into books (user_id, book_name, page_total, days_left) values (?, ?, ?, ?)", [user_id, book_name, page_total, days_left])
        connection.commit()
        return "Tracking book"
    
def delete_book(book_name):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    sql.execute("DELETE FROM books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name])
    return "Book deleted"


def locate_books():
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    result = sql.execute("SELECT book_name, page_total, days_left FROM books WHERE user_id = ?", [user_id])
    rows = result.fetchall()
    return rows