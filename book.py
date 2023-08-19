from flask import Blueprint, redirect, render_template, session, request, url_for
from bookself import add_book
from connection import get_db

book_bp= Blueprint('book', __name__)
    
@book_bp.route('/track', methods=['GET', 'POST'])
def track():
    error=""
    connection = get_db()
    sql = connection.cursor()
    if request.method == "POST":
        name=request.form['book-name']
        pages=request.form['num-pages']
        days=request.form['days']
        id=session.get('user_id')
        error=add_book(name,pages,days,id)
    return render_template('track.html')
    