from flask import Flask, redirect, render_template, request

app = Flask(__name__)

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
        for i in range(5):
            goal = request.form.get('goal' + str(i))
            goals.append(goal)
        return render_template('choose.html', goals=goals)


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
