from flask import Flask, render_template, redirect, request, session, url_for

from users import create_table
from book_data import create_books
from planned_book_data import create_planned_books
from finished_book_data import create_finished_books

from auth import auth_bp
from books import book_bp
from planned_books import planned_book_bp
from finished_book import finished_book_bp

app = Flask(__name__)

app.secret_key = "gUG*7BNmM*[*hUd7&y6hb}GlTcub`C"

app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)
app.register_blueprint(planned_book_bp)
app.register_blueprint(finished_book_bp)


with app.app_context():
    create_table()
    create_books()
    create_planned_books()
    create_finished_books()


@app.route('/', methods=['GET', 'POST'])
def home():
    if session.get("logged_in"): 
        return render_template('home.html')
    else:
        return redirect(url_for('auth.login_page'))