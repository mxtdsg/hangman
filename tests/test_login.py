import sys
sys.path.append('../')
from hangman.hangman import *
import unittest

class LoginTestCase(unittest.TestCase):
    # able to get to home/index page after set up
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    ## Test user login/logout

    # status after setup: not logged in
    def test_not_logged_in_after_set_up(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Please sign in!' in response.data)

    # able to log in successfully
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get(
            '/login',
            data=dict(username='test'),
            follow_redirects=True
        )
        self.assertTrue(b'Please sign in!' not in response.data)
        self.assertTrue(b'Welcome to the Hangman game!' in response.data)

    # able to log out successfully
    def test_logout(self):
        tester = app.test_client(self)
        response = tester.get(
            '/login',
            data=dict(username='test'),
            follow_redirects=True
        )
        self.assertTrue(b'Please sign in!' not in response.data)
        self.assertTrue(b'Welcome to the Hangman game!' in response.data)
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'Please sign in!' in response.data)

    # able to go to game when logged in
    def test_start_game_when_loggedin(self):
        tester = app.test_client(self)
        response = tester.get(
            '/login',
            data=dict(username='test'),
            follow_redirects=True
        )
        response = tester.get('/play', follow_redirects=True)
        self.assertTrue(b"You've Guessed:" in response.data)

    # go back home in the middle of the game: still logged in
    def test_keep_logged_in(self):
        tester = app.test_client(self)
        tester.get(
            '/login',
            data=dict(username='test'),
            follow_redirects=True
        )
        tester.get('/play', follow_redirects=True)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b'Please sign in!' not in response.data)
        self.assertTrue(b'Welcome to the Hangman game!' in response.data)

    # go to /play, /play/id when not logged in: would direct back home
    def test_access_game_when_not_loggedin(self):
        tester = app.test_client(self)
        response = tester.get('/play', follow_redirects=True)
        self.assertTrue(b'Please sign in!' in response.data)
        response = tester.get('/play/1', follow_redirects=True)
        self.assertTrue(b'Please sign in!' in response.data)

    # go to /play/other_players_id: would direct back home
    def test_access_others_game(self):
        tester = app.test_client(self)
        response = tester.get(
            '/login',
            data=dict(username='test'),
            follow_redirects=True
        )
        response = tester.get('/play/1000', follow_redirects=True)
        self.assertTrue(b'Please sign in!' not in response.data)
        self.assertTrue(b'Welcome to the Hangman game!' in response.data)


if __name__ == "__main__":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db = SQLAlchemy(app)
    db.drop_all()
    db.create_all()
    unittest.main()