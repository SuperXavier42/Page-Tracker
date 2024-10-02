from flask import Blueprint, redirect, render_template, session, request, url_for
from book_data import add_book, locate_books

book_bp = Blueprint('book', __name__)

@book_bp.route('/addbook', methods=['GET', 'POST'])
def addbook():
    notif=""
    if request.method == "POST":
        name=request.form['book-name']
        pages=request.form['num-pages']
        days=request.form['days']
        notif=add_book(name, pages, days)
    return render_template('addbook.html', error=notif)        
    
