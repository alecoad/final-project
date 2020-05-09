from flask import Flask, redirect, render_template, request

app = Flask(__name__)

goals = []

@app.route('/')
def index():
    return render_template('index.html', goals=goals)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        goal = request.form.get('goal')
        goals.append(goal)
        return redirect('/')
