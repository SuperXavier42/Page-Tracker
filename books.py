from flask import Blueprint, redirect, render_template, request, url_for
from book_data import add_book, locate_books, delete_book, complete_book


book_bp = Blueprint('book', __name__)

@book_bp.route('/reading', methods=['GET', 'POST'])
def current_books():
    books = locate_books()
    return render_template('reading.html', books=books)

@book_bp.route('/reading/addbook', methods=['GET', 'POST'])
def addbook():
    notif=""
    if request.method == "POST":
        name=request.form['book_name']
        pages=request.form['num_pages']
        days=request.form['days']
        if(pages.isnumeric() and days.isnumeric()):
            notif=add_book(name, pages, days)
        else:
            notif="Invalid Input"
    return render_template('addbook.html', error=notif)        
    
@book_bp.route('/reading/deletebook', methods=['GET', 'POST'])
def deletebook():
    if request.method == "POST":
        to_delete=request.form['book_name']
        delete_book(to_delete)
    return redirect(url_for('book.current_books'))

@book_bp.route('/reading/completedbook', methods=['GET', 'POST'])
def completebook():
    if request.method == "POST":
        to_complete=request.form['book_name']
    return render_template('completebook.html', book=to_complete)

@book_bp.route('/reading/submitcompletedbook', methods=['GET', 'POST'])
def submitcompletedbook():
    notif=""
    if request.method == "POST":
        name=request.form['book_name']
        pages=request.form['num_pages']
        if(pages.isnumeric()):
            complete_book(name, pages)
            return redirect(url_for('book.current_books'))
        else:
            notif="Invalid Input"
            return render_template('completebook.html', book=name, error=notif)