# Hangman

Hangman game implemented using python-flask

On this page:

* [Setup](#setup)
* [Logistics](#logistics)
* [Problems/Bugs](#problemsbugs)	
* [Extension Ideas](#extension-ideas)
* [Links/References](#linksreferences)

- - -

## Setup
1. Need: Python(2.7), flask, flask-SQLAlchemy

    To install flask on Ubuntu: `$ sudo pip install flask`
    
    To install SQLAlchemy on Ubuntu: `$ sudo pip install flask-sqlalchemy`
  
2. Run: `$ python hangman.py`
3. Visit http://localhost:5000 on browser

## Logistics
Includes the game and a scoreboard.

Used one table 'User' to record users' id, username, number of wins/loses, and the most recent game info, which includes: current guessing word, guesses, number of guesses left, whether the game has finished/won.

User only needs username to log in, and can resume an abandoned game.

Game supports keyboards input. User can only guess one alphabetical letter at a time.
When the game is won, a green Modal would pop, and a red one when lost. The actual word would be shown when finished. User would be given the chance to play again.

## Problems/Bugs
1. WordList includes words with special characters. (eg. "-", "()")
2. No auto-focus on the input box
3. Back to homepage lose username
4. Go to http://localhost:5000/play in the middle of a game, get a new game
5. white spaces
6. Test

## Extension Ideas
1. User can guess the whole word.
2. Mouse input: Adding buttons for all the letters.
3. Multiplayer mode.
4. Categories for words.
5. Add Play Agian button to Modal.
6. Prompt message on: special characters, already guessed letters.
7. Access control: Need passwords to login.

## Links/References
1. WordList: http://www-personal.umich.edu/~jlawler/wordlist.html
2. Bootstrap template: https://getbootstrap.com/docs/4.0/examples/starter-template/
3. W3School Modal: https://www.w3schools.com/w3css/w3css_modal.asp
