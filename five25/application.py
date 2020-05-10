from flask import Flask, redirect, render_template, request, session

from flask_session import Session

app = Flask(__name__)

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

topfive = []
goals = []

@app.route('/')
def index():
    return render_template('index.html', topfive=topfive, goals=goals)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if session.get('goals') is None:
        session['goals'] = []
    if request.method == 'POST':
        goal = request.form.get('goal')
        session['goals'].append(goal)

    return render_template('create.html', goals=session['goals'])


@app.route('/choose', methods=['POST'])
def choose():
    toplist = request.form.getlist('goal')
    for i in toplist:
        topfive.append(i)
        goals.remove(i)
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
