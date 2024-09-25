from flask import Flask, render_template, redirect, request, session, url_for
from users import create_table
from book_data import create_books
from auth import auth_bp
from books import book_bp

app = Flask(__name__)

app.secret_key = "gUG*7BNmM*[*hUd7&y6hb}GlTcub`C"

app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)



with app.app_context():
    create_table()
    create_books()

@app.route('/')
def home():
    if session.get("logged_in"): 
        user_id = session.get('user_id')
        return render_template('home.html')
    else:
        return redirect(url_for('auth.login_page'))
        