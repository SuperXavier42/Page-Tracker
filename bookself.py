from flask import Blueprint, redirect, render_template, session, request, url_for

from connection import get_db

def setup_book():
    connection = get_db()
    sql = connection.cursor()
    sql.execute('''create table if not exists books
    (
        userId integer,
        bookId integer primary key autoincrement,
        bookName Text,
        bookPages integer,
        days integer,
        FOREIGN KEY (userId) REFERENCES users (id)
    )''')
    
def add_book(name, pages, days, id):    
    connection = get_db()
    sql = connection.cursor()
    result = sql.execute("select * from books where userId = ? AND bookName = ?", [id, name])
    rows = result.fetchall()
    if len(rows) > 0:
        return "Exisiting book"
    else:
        sql.execute("insert into books (userId, bookName, bookPages, days) values (?, ?, ?, ?)", [id, name, pages, days])
        connection.commit()
        return "Book added"