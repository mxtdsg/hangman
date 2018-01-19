from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)

word = "BERKELEY"
guesses = []


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/play')
# def play():
#     return render_template('play.html', word = check(word, guesses))

# def random10():
#     return random.randrange(10)
def randomword():
    return "BERKELEY"

def check(word, guesses):
    re = ''
    for char in word:
        if char in guesses:
            re += char
        else:
            re += "*"
    return re

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        letter = request.form['letter'].upper()
        print letter
        guesses.append(letter)
    return render_template('play.html', word = check(word, guesses))



app.debug = True

if __name__ == '__main__':
    app.run()