from flask import Blueprint, redirect, render_template, request, url_for
from planned_book_data import add_book, start_book, delete_book, locate_books

planned_book_bp = Blueprint('planned', __name__)

@planned_book_bp.route('/planning', methods=['GET', 'POST'])
def future_books():
    books=locate_books()
    return render_template('planning.html', books=books)

@planned_book_bp.route('/planning/addbook', methods=['GET', 'POST'])
def addbook():
    notif=""
    if request.method == "POST":
        name=request.form['book_name']
        notif=add_book(name)
    return render_template('planbook.html', error=notif)        
    
@planned_book_bp.route('/planning/deletebook', methods=['GET', 'POST'])
def deletebook():
    if request.method == "POST":
        to_delete=request.form['book_name']
        delete_book(to_delete)
    return redirect(url_for('planned.future_books'))

@planned_book_bp.route('/planning/startbook', methods=['GET', 'POST'])
def startbook():
    if request.method == "POST":
        to_start=request.form['book_name']
    return render_template('startbook.html', book=to_start)

@planned_book_bp.route('/planning/submitstartedbook', methods=['GET', 'POST'])
def submitstartedbook():
    if request.method == "POST":
        name=request.form['book_name']
        pages=request.form['num_pages']
        days=request.form['days']
        start_book(name, pages, days)
    return redirect(url_for('planned.future_books'))