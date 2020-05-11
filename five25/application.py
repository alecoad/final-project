import os

from flask import flash, Flask, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

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
def index():
    if session.get('goals') is None:
        session['goals'] = []
    if session.get('toplist') is None:
        session['toplist'] = []
    return render_template('index.html', toplist=session['toplist'], goals=session['goals'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = :username', {'username': username}
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect('/')

        flash(error)
        print(error)

    return render_template('register.html')



@app.route('/create', methods=['GET', 'POST'])
def create():
    if session.get('goals') is None:
        session['goals'] = []
    if request.method == 'POST':
        goal = request.form.get('goal')
        session['goals'].append(goal)

    return render_template('create.html', goals=session['goals'])


@app.route('/choose', methods=['GET', 'POST'])
def choose():
    print(session.get('goals'))
    if request.method == 'GET':
        if session.get('goals') is None:
            redirect('/create')
        return render_template('choose.html', goals=session['goals'])

    else:
        session['toplist'] = []
        topgoals = request.form.getlist('goal')
        for goal in topgoals:
            session['toplist'].append(goal)
            session['goals'].remove(goal)

        return redirect('/')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        goal = request.form.get('goal')
        goals.append(goal)
        return redirect('/')

@app.route('/logout')
def logout():
    """Log user out"""
    session.clear()
    return redirect('/')
