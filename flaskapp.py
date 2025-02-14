from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

#SQLite setup
connection = sqlite3.connect('lab2_database.db')
cursor = connection.cursor()
cursor.execute("'CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, first_name TEXT NOT NULL, last_name TEXT NOT NULL, address TEXT NOT NULL)'"
)
connection.commit()
connection.close()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    address = request.form['address']

    connection = sqlite3.connect('lab2_database.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO users (username, password, email, first_name, last_name, address) VALUES ({username}, {password}, {email}, {first_name}, {last_name}, {address})")
    connection.commit()
    connection.close()

    return redirect(url_for('profile', username=username))

@app.route('/profile/<username>')
def profile(username):
    connection = sqlite3.connect('lab2_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    cursor = user.fetchone()
    connection.close()

    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
