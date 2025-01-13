from flask import Blueprint, redirect, render_template, request, url_for
from planned_book_data import add_book, start_book, delete_book, locate_books

#this file has all the routes that the user interacts with to use the data modifying functions

planned_book_bp = Blueprint('planned', __name__)

#route for main planning interface
@planned_book_bp.route('/planning', methods=['GET', 'POST'])
def future_books():
    books=locate_books()
    return render_template('planning/planning.html', books=books)

#route for addbook and adds a book if a post request is made via form
@planned_book_bp.route('/planning/addbook', methods=['GET', 'POST'])
def addbook():
    notif=""
    if request.method == "POST":
        name=request.form['book_name']
        notif=add_book(name)
    return render_template('planning/planbook.html', error=notif)        
    
#deletes book after requesting name 
@planned_book_bp.route('/planning/deletebook', methods=['GET', 'POST'])
def deletebook():
    if request.method == "POST":
        to_delete=request.form['book_name']
        delete_book(to_delete)
    return redirect(url_for('planned.future_books'))

#requests name and then renders the startbook page
@planned_book_bp.route('/planning/startbook', methods=['GET', 'POST'])
def startbook():
    if request.method == "POST":
        to_start=request.form['book_name']
        page_count=request.form['page-count']
        if(int(page_count)>0):
            return render_template('planning/continuebook.html', book=to_start, pages=page_count)
    return render_template('planning/startbook.html', book=to_start)

#requests all the data from the startbook page and then uses start_book to add the data to the data table
@planned_book_bp.route('/planning/submitstartedbook', methods=['GET', 'POST'])
def submitstartedbook():
    notif=""
    if request.method == "POST":
        name=request.form['book_name']
        pages=request.form['num_pages']
        days=request.form['days']
        if(pages.isnumeric() and days.isnumeric()):
            start_book(name, pages, days)
            return redirect(url_for('planned.future_books'))
        else:
            notif="Invalid Input"
            return render_template("planning/startbook.html", book=name, error=notif)