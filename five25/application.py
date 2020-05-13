import os
import requests

from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

topfive = []
goals = []

@app.route('/')
@login_required
def index():
    # get user id
    user_id = session['user_id']
    # query for true goals
    tasks = db.execute(
        'SELECT name FROM tasks WHERE user_id = :user_id AND distraction = FALSE', {'user_id': user_id}
    ).fetchall()
    # query for distractions
    distractions = db.execute(
        'SELECT name FROM tasks WHERE user_id = :user_id AND distraction = TRUE', {'user_id': user_id}
    ).fetchall()

    return render_template('index.html', tasks=tasks, distractions=distractions)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirmation:
            error = 'Password and confirmation must match.'
        elif db.execute(
            'SELECT id FROM users WHERE username = :username', {'username': username}
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO users (username, password) VALUES (:username, :password)',
                {'username': username, 'password': generate_password_hash(password)}
            )
            db.commit()

            # Remember user
            user = db.execute(
                'SELECT * FROM users WHERE username = :username', {'username': username}
            ).fetchone()
            session['user_id'] = user['id']
            print(session['user_id'])

            return redirect('/')

        #flash(error)
        print(error)

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = :username', {'username': username}
        ).fetchone()
        print(user)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            print(user['id'])
            return redirect('/')

        #flash(error)
        print(error)

    return render_template('login.html')


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # get user id
    user_id = session['user_id']

    if request.method == 'POST':
        task = request.form.get('goal')
        db.execute(
            'INSERT INTO tasks (name, user_id) VALUES (:task, :user_id)', {'task': task, 'user_id': user_id}
        )
        db.commit()

    tasks = db.execute(
        'SELECT name FROM tasks WHERE user_id = :user_id', {'user_id': user_id}
    ).fetchall()

    return render_template('create.html', tasks=tasks)


@app.route('/choose', methods=['GET', 'POST'])
@login_required
def choose():
    # get user id
    user_id = session['user_id']

    if request.method == 'POST':
        # store the checked goals
        priorities = request.form.getlist('task')
        # change 'distraction' to FALSE for each chosen goal
        for priority in priorities:
            db.execute(
                'UPDATE tasks SET distraction = FALSE WHERE user_id = :user_id AND name = :priority', {'user_id': user_id, 'priority': priority}
            )
            print(priority)
        db.commit()

        return redirect('/')

    # check that goals exist
    if db.execute(
        'SELECT name FROM tasks WHERE user_id = :user_id', {'user_id': user_id}
    ).fetchone() is None:
        redirect('/create')

    # query for all goals from user
    tasks = db.execute(
        'SELECT name FROM tasks WHERE user_id = :user_id', {'user_id': user_id}
    ).fetchall()
    # display goals for user to choose
    return render_template('choose.html', tasks=tasks)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/logout')
def logout():
    """Log user out"""
    session.clear()
    return redirect('/')
