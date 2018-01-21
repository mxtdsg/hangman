
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hangman.db'

db = SQLAlchemy(app)



class User(db.Model):
    # user info
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    wins = db.Column(db.Integer, default=0)
    loses = db.Column(db.Integer, default=0)
    # most recent game info
    cur_word = db.Column(db.String(50))
    cur_guesses = db.Column(db.String(50), default='')
    finished = db.Column(db.Boolean, default=False)
    win = db.Column(db.Boolean, default=False)
    times_left = db.Column(db.Integer, default=10)


    def __init__(self, username):
        self.username = username
        self.cur_word = self.random_word()

    def new_game(self):
        self.finished = False
        self.cur_word = self.random_word()
        self.cur_guesses = ''
        self.win = False
        self.times_left = 10

    def try_letter(self, letter):
        if len(letter) != 1:
            return
        elif letter in self.cur_guesses:
            return
        
        self.cur_guesses += letter
        if letter not in self.cur_word:
            self.times_left -= 1

        if self.times_left <= 0:
            self.finished = True
            self.loses += 1
        db.session.commit()

    @property
    def render(self):
        rendered = ''.join([char if char in self.cur_guesses else '*' for char in self.cur_word])
        print rendered
        if rendered == self.cur_word:
            self.win = True
            self.finished = True
            self.wins+=1
            db.session.commit()
        return rendered


    def random_word(self):
        words = [line.strip() for line in open("wordlist.txt")]
        return random.choice(words).upper()




@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/play')
def new_game():
    print "hererereerer"
    username = request.args.get('username')
    # check if user exist
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return redirect(url_for('play', user_id=user.id))
    # if not create new user
    user = User(username)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('play', user_id=user.id))


@app.route('/play/<user_id>', methods=['GET', 'POST'])
def play(user_id):
    user = User.query.get(user_id)
    if user.finished:
        user.new_game()
        db.session.commit()
    if request.method == 'POST':
        letter = request.form['letter'].upper()
        user.try_letter(letter)
    return render_template('play.html', user=user)




app.debug = True

if __name__ == '__main__':
    app.run()