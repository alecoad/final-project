from flask import Flask, redirect, render_template, request

app = Flask(__name__)

goals = []

@app.route('/')
def index():
    return render_template('index.html', goals=goals)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    else:
        for i in range(3):
            goal = request.form.get('goal' + str(i))
            goals.append(goal)
        return redirect('/')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        goal = request.form.get('goal')
        goals.append(goal)
        return redirect('/')
