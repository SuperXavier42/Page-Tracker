from flask import Blueprint, redirect, render_template, request, url_for
from book_data import add_book, locate_books, delete_book, complete_book

#this file has all the routes that the user interacts with to use the data modifying functions

book_bp = Blueprint('book', __name__)

#route for current books page
@book_bp.route('/reading', methods=['GET', 'POST'])
def current_books():
    books = locate_books()
    return render_template('current/reading.html', books=books)

#route for adding books to current database
@book_bp.route('/reading/addbook', methods=['GET', 'POST'])
def addbook():
    notif=""
    #requests all the data from the page and then uses add_book to add to the database
    if request.method == "POST":
        name=request.form['book_name']
        pages=request.form['num_pages']
        days=request.form['days']
        if(pages.isnumeric() and days.isnumeric()):
            notif=add_book(name, pages, days)
        else:
            notif="Invalid Input"
    return render_template('current/addbook.html', error=notif)        

#route to get the name of the book being deleted and then calls the delete function
@book_bp.route('/reading/deletebook', methods=['GET', 'POST'])
def deletebook():
    if request.method == "POST":
        to_delete=request.form['book_name']
        delete_book(to_delete)
    return redirect(url_for('book.current_books'))

#route to get the name of the book being completed and then renders the template for the complete book page
@book_bp.route('/reading/completedbook', methods=['GET', 'POST'])
def completebook():
    if request.method == "POST":
        to_complete=request.form['book_name']
    return render_template('current/completebook.html', book=to_complete)

#route to get the name of book and the page number to use the complete book function
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
            return render_template('current/completebook.html', book=name, error=notif)