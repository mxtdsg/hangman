from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

"""
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), default="xxx")
    wins = db.Column(db.Integer, default=0)
    loses = db.Column(db.Integer, default=0)
    def __init__(self, username):
        self.username = username


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer)
    username = db.Column(db.String(10))
    word = db.Column(db.String(50), default="BERKELEY")
    guesses = db.Column(db.String(50), default='')
    win = db.Column(db.Boolean, default=False)

    # def __init__(self, user_id):
        # self.user_id = user_id
    def __init__(self, username):
        self.username = username

    def try_letter(self, letter):
        self.guesses += letter
        db.session.commit()

    @property
    def render(self):
        rendered = ''.join([char if char in self.guesses else ' _ ' for c in self.word])
        if rendered == word:
            win = True
            user = User.query.get(user_id)
            user.wins+=1
            db.session.commit()
        return rendered

    # @property
    # def game_finished(self):



def random_word():
    return "BERKELEY"




@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/play')
def new_game():
    # game = Game()
    # game = Game(request.args.get('user'))
    user = request.args.get('user')
    user = User(user)
    session['user_id'] = user.id
    
    game = Game(user.username)
    db.session.add(game)
    db.session.commit()
    return redirect(url_for('play', game_id=game.id))


@app.route('/play/<game_id>', methods=['GET', 'POST'])
def play(game_id):
    game = Game.query.get(game_id)
    if request.method == 'POST':
        letter = request.form['letter'].upper()
        game.try_letter(letter)
    return render_template('play.html', game=game)





app.debug = True

if __name__ == '__main__':
    app.run()