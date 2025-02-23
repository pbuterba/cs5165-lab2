"""
@package    flaskapp
@brief      Powers a basic registration form for a page as part of Lab 2 for University of Cincinnati's CS 5165 - Intro
            to Cloud Computing Class (Spring 2025)

@date       2/11/2025
@updated    2/14/2025

@author     Preston Buterbaugh
@credit     https://uc.instructure.com/courses/1737794/assignments/22046538
"""

import os

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE_PATH = os.path.join(PROJECT_ROOT, 'lab2_database.db')

app = Flask(__name__)

# SQLite setup
try:
    setup_connection = sqlite3.connect(DATABASE_PATH)
    setup_cursor = setup_connection.cursor()
    setup_cursor.execute(
        """CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, first_name TEXT NOT NULL, last_name TEXT NOT NULL, address TEXT NOT NULL)"""
    )
    setup_connection.commit()
    setup_connection.close()
except sqlite3.OperationalError:
    print('Unable to open database file')


@app.route('/')
def index():
    return render_template('register.html')


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    entered_password = request.form['password']

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    correct_password = cursor.fetchone()[0]
    connection.close()

    if correct_password is None:
        return 'Invalid username'

    if entered_password == correct_password:
        return redirect(url_for('profile', username=username))
    else:
        return 'Incorrect password'


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    address = request.form['address']

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO users (username, password, email, first_name, last_name, address) VALUES (?, ?, ?, ?, ?, ?)", (username, password, email, first_name, last_name, address,))
    connection.commit()
    connection.close()

    return redirect(url_for('profile', username=username))


@app.route('/profile/<username>')
def profile(username):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    connection.close()

    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
