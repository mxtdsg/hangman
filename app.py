from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)



class Game(db.Model):
    # user info
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    wins = db.Column(db.Integer, default=0)
    loses = db.Column(db.Integer, default=0)
    # most recent game
    cur_word = db.Column(db.String(50), default="BERKELEY")
    cur_guesses = db.Column(db.String(50), default='')
    finished = db.Column(db.Boolean, default=False)


    def __init__(self, username):
        self.username = username

    def new_game(self):
        self.finished = False
        self.cur_word = "STANFORD"
        self.cur_guesses = ''

    def try_letter(self, letter):
        self.cur_guesses += letter
        db.session.commit()

    @property
    def render(self):
        rendered = ''.join([char if char in self.cur_guesses else ' _ ' for char in self.cur_word])
        if rendered == self.cur_word:

            self.finished = True
            self.wins+=1
            db.session.commit()
        return rendered




def random_word():
    return "BERKELEY"




@app.route('/')
def index():
    users = Game.query.all()
    return render_template('index.html', users=users)


@app.route('/play')
def new_game():
    username = request.args.get('username')

    user = Game.query.filter_by(username=username).first()
    if user is not None:
        return redirect(url_for('play', game_id=user.id))


    game = Game(username)
    db.session.add(game)
    db.session.commit()
    return redirect(url_for('play', game_id=game.id))


@app.route('/play/<game_id>', methods=['GET', 'POST'])
def play(game_id):
    game = Game.query.get(game_id)
    if game.finished:
        game.new_game()
    if request.method == 'POST':
        letter = request.form['letter'].upper()
        game.try_letter(letter)
    return render_template('play.html', game=game)




app.debug = True

if __name__ == '__main__':
    app.run()