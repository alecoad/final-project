from flask import Flask, redirect, render_template, request, session

from flask_session import Session

app = Flask(__name__)

# configure session to use filesystem (instead of signed cookies)
#app.config["SESSION_FILE_DIR"] = mkdtemp()
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

goals = []
topfive = []

@app.route('/')
def index():
    print(topfive)
    print(goals)
    return render_template('index.html', topfive=topfive, goals=goals)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    else:
        goal = request.form.get('goal')
        goals.append(goal)
        return render_template('create.html', goals=goals)


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
