from flask import Blueprint, redirect, render_template, request, url_for
from book_data import add_book, locate_books, delete_book, complete_book


book_bp = Blueprint('book', __name__)

@book_bp.route('/addbook', methods=['GET', 'POST'])
def addbook():
    notif=""
    if request.method == "POST":
        name=request.form['book_name']
        pages=request.form['num_pages']
        days=request.form['days']
        notif=add_book(name, pages, days)
    return render_template('addbook.html', error=notif)        
    
@book_bp.route('/deletebook', methods=['GET', 'POST'])
def deletebook():
    if request.method == "POST":
        to_delete=request.form['book_name']
        delete_book(to_delete)
    return redirect(url_for('book.current_books'))

@book_bp.route('/completedbook', methods=['GET', 'POST'])
def completebook():
    if request.method == "POST":
        to_complete=request.form['book_name']
        complete_book(to_complete)
    return redirect(url_for('book.current_books'))

@book_bp.route('/reading', methods=['GET', 'POST'])
def current_books():
    books = locate_books()
    return render_template('reading.html', books=books)

@book_bp.route('/planning', methods=['GET', 'POST'])
def future_books():
    return redirect(url_for('home'))