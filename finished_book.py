from flask import redirect, render_template, Blueprint, url_for, request
from finished_book_data import add_book, delete_book, locate_books

#this file has all the routes that the user interacts with to use the data modifying functions

finished_book_bp = Blueprint('finished', __name__)

@finished_book_bp.route('/finished', methods=['GET', 'POST'])
def finished_books():
    books=locate_books()
    return render_template('finished/finished.html', books=books)

@finished_book_bp.route('/finished/addbook', methods=['GET', 'POST'])
def addbook():
    notif=""
    if request.method == "POST":
        name=request.form['book_name']
        date=request.form['date_finished']
        notif=add_book(name,date)
    return render_template("finished/addfinishedbook.html", error=notif)

@finished_book_bp.route('/finished/deletebook', methods=['GET', 'POST'])
def deletebook():
    if request.method == "POST":
        name=request.form['book_name']
        delete_book(name)
    return redirect(url_for('finished.finished_books'))