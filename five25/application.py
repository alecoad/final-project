import os
import requests

from flask import flash, Flask, jsonify, redirect, render_template, request, session
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
    # query all the user's lists
    lists = db.execute(
        'SELECT * FROM lists WHERE user_id = :user_id', {'user_id': user_id}
    ).fetchall()

    #fix later
    list_id = 1
    # query for focused tasks
    focus = db.execute(
        'SELECT name FROM tasks WHERE list_id = :list_id AND distraction = FALSE', {'list_id': list_id}
    ).fetchall()
    # query for distractions
    distractions = db.execute(
        'SELECT name FROM tasks WHERE list_id = :list_id AND distraction = TRUE', {'list_id': list_id}
    ).fetchall()
    # query for completed tasks
    completed = db.execute(
        'SELECT name FROM tasks WHERE list_id = :list_id AND completed = TRUE', {'list_id': list_id}
    ).fetchall()
    print(focus)
    print(distractions)
    print(completed)

    return render_template('index.html', lists=lists, focus=focus, distractions=distractions, completed=completed)

@app.route('/tasks/<int:list_id>')
@login_required
def tasks(list_id):
    # get user id
    user_id = session['user_id']
    # query for focused tasks
    focus = db.execute(
        'SELECT name FROM tasks WHERE list_id = :list_id AND distraction = FALSE', {'list_id': list_id}
    ).fetchall()
    # query for distractions
    distractions = db.execute(
        'SELECT name FROM tasks WHERE list_id = :list_id AND distraction = TRUE', {'list_id': list_id}
    ).fetchall()
    # query for completed tasks
    completed = db.execute(
        'SELECT name FROM tasks WHERE list_id = :list_id AND completed = TRUE', {'list_id': list_id}
    ).fetchall()
    print(focus)
    print(distractions)
    print(completed)

    return render_template('tasks.html', focus=focus, distractions=distractions, completed=completed)


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

        flash(error)
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

        flash(error)
        print(error)

    return render_template('login.html')


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # get user id
    user_id = session['user_id']

    if request.method == 'POST':
        # PROBABLY NEED SOME ERROR HANDLING...
        # store and insert title into lists table
        title = request.form.get('title')
        db.execute(
            'INSERT INTO lists (title, user_id) VALUES (:title, :user_id)', {'title': title, 'user_id': user_id}
        )
        # get list_id
        list_id = db.execute(
            'SELECT id FROM lists WHERE title = :title', {'title': title}
        ).fetchone()
        # get the id of the tuple since fetchone() returns a Row-like object
        list_id = list_id[0]
        # store and enter each task into tasks table
        tasks = request.form.getlist('task')
        for task in tasks:
            db.execute(
                'INSERT INTO tasks (name, list_id) VALUES (:task, :list_id)', {'task': task, 'list_id': list_id}
            )
        db.commit()
        # store all the tasks (UNNECESSARY?)
        tasks = db.execute(
            'SELECT name FROM tasks WHERE list_id = :list_id', {'list_id': list_id}
        ).fetchall()
        return render_template('focus.html', list_id=list_id, tasks=tasks)

    return render_template('create.html')


@app.route('/focus', methods=['GET', 'POST'])
@login_required
def focus():
    # get user id
    user_id = session['user_id']
    # get list_id
    list_id = db.execute(
        'SELECT id FROM lists WHERE user_id = :user_id', {'user_id': user_id}
    ).fetchone()
    # get the id of the tuple since fetchone() returns a Row-like object
    list_id = list_id[0]

    if request.method == 'POST':
        # store the checked goals
        priorities = request.form.getlist('task')
        # change 'distraction' to FALSE for each chosen goal
        for priority in priorities:
            db.execute(
                'UPDATE tasks SET distraction = FALSE WHERE list_id = :list_id AND name = :priority', {'list_id': list_id, 'priority': priority}
            )
            print(priority)
        db.commit()

        return redirect('/')

    # check that goals exist
    if db.execute(
        'SELECT name FROM tasks WHERE list_id = :list_id', {'list_id': list_id}
    ).fetchone() is None:
        redirect('/create')

    # query for all tasks in the list
    tasks = db.execute(
        'SELECT name FROM tasks WHERE list_id = :list_id', {'list_id': list_id}
    ).fetchall()
    # display goals for user to narrow focus
    return render_template('focus.html', tasks=tasks)


@app.route('/complete')
def complete():
    return redirect('/')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/logout')
def logout():
    """Log user out"""
    session.clear()
    return redirect('/')
