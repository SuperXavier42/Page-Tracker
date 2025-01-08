from flask import session
from connection import get_db_tuple
from datetime import datetime, timedelta

def create_books():
    connection = get_db_tuple()
    sql = connection.cursor()
    sql.execute(
        """create table if not exists books (
        "user_id" Integer,
        "book_name" Text,
        "page_total" Integer,
        "pages_read" Integer,
        "days_left" Integer,
        "target_date" String
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
        if(int(days_left)>0 and int(page_total)>0):
            date=datetime.now()
            target_date=date + timedelta(days=int(days_left)+1)
            target_date = target_date.replace(hour=0, minute=0, second=0)
            sql.execute("INSERT into books (user_id, book_name, page_total, pages_read, days_left, target_date) VALUES (?, ?, ?, ?, ?, ?)", [user_id, book_name, page_total, 0, days_left, target_date])
            connection.commit()
            return "Tracking book"
        else:
            return "Invalid Input"
    
def delete_book(book_name):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    sql.execute("DELETE FROM books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name])
    connection.commit()
    return "Book deleted"

def complete_book(book_name, page_num):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    total_pages = sql.execute("SELECT page_total FROM books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name]).fetchone()[0]
    if(total_pages-int(page_num) <= 0):
        sql.execute("DELETE FROM books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name])
    else:
        sql.execute("UPDATE books SET pages_read = ? WHERE (user_id = ? AND book_name = ?)", [page_num, user_id, book_name])
    connection.commit()
    return "Book completed"

def locate_books():
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    names = sql.execute("SELECT book_name FROM books WHERE user_id = ?", [user_id]).fetchall()
    for book in names:
        days_remaining(book[0])
    result = sql.execute("SELECT book_name, page_total, pages_read, days_left FROM books WHERE user_id = ?", [user_id])
    rows = result.fetchall()
    return rows

def days_remaining(book_name):
    connection = get_db_tuple()
    sql = connection.cursor()
    user_id = session.get('user_id')
    result = sql.execute("SELECT target_date, page_total FROM books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name])
    row=result.fetchone()
    target_date = datetime.strptime(row[0][0:19], '%Y-%m-%d %H:%M:%S')
    days_left=target_date - datetime.now()
    if(days_left.days<=0):
        sql.execute("DELETE FROM books WHERE (user_id = ? AND book_name = ?)", [user_id, book_name])
        sql.execute("INSERT into planned_books (user_id, book_name, page_count) VALUES (?, ?, ?)", [user_id, book_name, row[1]])
    else:
        sql.execute("UPDATE books SET days_left = ? WHERE (user_id = ? AND book_name = ?)", [int(days_left.days), user_id, book_name])
    connection.commit()
    return "Day updated"
