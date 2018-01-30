# Hangman

Hangman game implemented using python-flask

On this page:

* [Setup](#setup)
* [Logistics](#logistics)
* [Problems/Bugs](#problemsbugs)
* [Tests](#tests)
* [Extension Ideas](#extension-ideas)
* [Links/References](#linksreferences)

- - -

## Setup
1. Need: Python(2.7), flask, flask-SQLAlchemy

    To install flask on Ubuntu: `$ sudo pip install flask`
    
    To install SQLAlchemy on Ubuntu: `$ sudo pip install flask-sqlalchemy`
  
2. Run: `$ python hangman.py`
3. Visit http://localhost:5000 on browser
4. Internet access is needed for the bootstrap templates

## Logistics
Includes the game and a scoreboard.

Used one table 'User' to record users' id, username, number of wins/loses, and the most recent game info, which includes: current guessing word, guesses, number of guesses left, whether the game has finished/won.

User only needs username to log in, and can resume an abandoned game.

Game supports keyboards input. User can only guess one alphabetical letter at a time.
When the game is won, a green Modal would pop, and a red one when lost. The actual word would be shown when finished. User would be given the chance to play again.

## Problems/Bugs
Solved:
1. No auto-focus on the input box
2. Back to homepage lose username
3. Go to http://localhost:5000/play in the middle of a game would get a new user/game
Sol: Added route to ask to login first, otherwise redirect back to homepage
4. Go to http://localhost:5000/play when not logged in would get a new user/game
5. Go to http://localhost:5000/play/<id> go directly to other people's game
6. Trailling white spaces/ Format and style
7. WordList includes words with special characters. (eg. "-", "()")
Sol: Random till we find a alphabetical word
8. Test
    
## Tests
To run all test cases: at root directory `$ python tests/test_game.py`

1. test_login: Test login/logout.
    Includes:
        test setup;
        test status after setup: not logged in;
        test able to log in successfully;
        test able to log out successfully;
        test able to go to game when logged in;
        test go back home in the middle of the game: still logged in;
        test go to /play, /play/id when not logged in: would direct back home;
        test go to /play/other_players_id: would direct back home.
2. test_game: Test game and scoreboard.
    Includes:
        test guess new letter in the word;
        test guess new letter not in the word;
        test guess already guessed letter / non alphabetical letter;
        test scoreboard track wins;
        test scoreboard track loses.

## Extension Ideas
1. User can guess the whole word.
2. Mouse input: Adding buttons for all the letters.
3. Multiplayer mode.
4. Categories for words.
5. Add Play Agian button to Modal.
6. Prompt message on: special characters, already guessed letters, when not logged in, when trying to access other ppl's games
7. Access control: Need passwords to login.
8. Show username on welcome page/top-right coner when in session 

## Links/References
1. WordList: http://www-personal.umich.edu/~jlawler/wordlist.html
2. Bootstrap template: https://getbootstrap.com/docs/4.0/examples/starter-template/
3. W3School Modal: https://www.w3schools.com/w3css/w3css_modal.asp
