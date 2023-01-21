from .connection import get_db
from passlib.hash import pbkdf2_sha256 as pw

def create_table():
    connection = get_db()
    sql = connection.cursor()
    sql.execute("""create table if not exists users (
        "id" integer primary key autoincrement,
        "username" Text,
        "password" Text) """)


def create_account(username, password):
    connection = get_db()
    sql = connection.cursor()
    hashed = pw.hash(password)
    sql.execute("insert into users (username, password) values (?, ?)",[username, hashed])   
    connection.commit()
    return "Account created"

def check_account(username, password):
    connection = get_db()
    sql = connection.cursor()
    result = sql.execute('''select * from users where username = ?''', [username])
    data = result.fetchone()
    if data:
        hashed = data['password']
        check_hash = pw.verify(password, hashed)
        if check_hash:
            return data['id']
    else:
        return False