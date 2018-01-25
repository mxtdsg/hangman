"""
Todo:
9. username length?

13. css local file?
14. docs

15. write up

16. prompt when not logged in try to play

17. prompt when play other's game




Finished:
5. random word
8. after lose show the acutal word
12. add button to play again after finishing a game
19. fixed bug, commit after reset new game.
18. new game at start word length not right
6. draw 
1. promote if len(letter) != 1
3. show already guessed letters
4. should only be able to guess english letters
20. print statement
16. clean db



Fine?:
7. clean db?
17 refresh the page after the game is done cause problem
2. promote if already guessed
10. now we can still resume the game
11. no access control

"""


from flask import Flask, render_template, request, redirect, url_for, session, flash, g, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hangman.db'
app.static_url_path=app.config.get('STATIC_FOLDER')
app.static_folder=app.root_path + app.static_url_path
db = SQLAlchemy(app)

app.secret_key = 'bluhbluh'


"""
User class: including user info(username, number of wins/loses), and most recent game info.

Methods: new_game(): reset all the most game info
        try_letter(letter): guess to see if the letter is in the word
        render(): render string (eg. E _ _ )
        random_word(): find a random alphabetical word from 'wordlist.txt'
"""
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
        if len(letter) != 1 or not letter.isalpha():
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
        # print self.cur_word
        rendered = ''.join([char if char in self.cur_guesses else '_' for char in self.cur_word])
        if rendered == self.cur_word:
            self.win = True
            self.finished = True
            self.wins+=1
            db.session.commit()
        return rendered

    def random_word(self):
        words = [line.strip() for line in open("wordlist.txt")]
        re = random.choice(words).upper()
        while not re.isalpha():
            re = random.choice(words).upper()
        return re


"""
Routing:

before_request(): check if user has logged in
index(): homepage with scoreboard and place to sign in
login(): sign up/log in
new_game(): direct user to his own game, and back to honepage otherwise
play(user_id): direct user to his own game, and back to honepage otherwise
logout(): log out user and direct back to homepage
"""
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session["user"]


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/login')
def login():
    # check if user exist
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user is not None:
        session['user'] = user.id
        return redirect(url_for('index'))
    # if not create new user
    user = User(username)
    db.session.add(user)
    db.session.commit()
    session['user'] = user.id
    return redirect(url_for('index'))

@app.route('/play')
def new_game():
    if g.user:
        return redirect(url_for('play', user_id=g.user))
    return redirect(url_for('index'))

@app.route('/play/<user_id>', methods=['GET', 'POST'])
def play(user_id):
    # go to /play when not logged in OR try to play other ppl's game
    if not g.user or g.user != int(user_id):
        return redirect(url_for('index'))
    user = User.query.get(user_id)
    if user.finished:
        user.new_game()
        db.session.commit()
    if request.method == 'POST':
        letter = request.form['letter'].upper()
        user.try_letter(letter)
    return render_template('play.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


app.debug = True
if __name__ == '__main__':
    app.run()