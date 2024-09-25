from flask import session
from connection import get_db

def create_books():
    connection = get_db()
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
    connection = get_db()
    sql = connection.cursor()
    user_id = session.get('user_id')
    result = sql.execute("select * from books where (user_id = ? AND book_name = ?)", [user_id, book_name])
    rows = result.fetchall()
    if(len(rows)>0):
        return "Book already being tracked"
    else:
        sql.execute("insert into books (user_id, book_name, page_total, days_left) values (?, ?, ?, ?)", [user_id, book_name, page_total, days_left])
        connection.commit()
        return "Tracking book"
    
def locate_books(user_id):
    connection = get_db()
    sql = connection.cursor()
    user_id = session.get('user_id')
    result = sql.execute("select (book_name, page_total, days_left) from books where user_id = ?", [user_id])
    rows = result.fetchall()
    return rows