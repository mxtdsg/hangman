from test_login import *

class GameTestCase(unittest.TestCase):
    ## Test game

    # guess new letter in the word: same number of guesses left; 1 more len(guesses); less '_' in render
    def test_guess_right_letter(self):
        with app.test_client(self) as tester:
            tester.get(
                '/login',
                data=dict(username='test'),
                follow_redirects=True
            )
            tester.get('/play', follow_redirects=True)
            user = User.query.get(g.user)
            ori_times_left = user.times_left
            ori_guesses = user.cur_guesses
            ori_guesses_len = len(ori_guesses)
            ori_white_spaces = user.render.count('_')
            for char in "zxcvbqpoieawuyrtmnblkjhgfds".upper():
                if char in user.cur_word and char not in ori_guesses:
                    response = tester.post(
                        '/play/'+str(g.user),
                        data=dict(letter=char),
                        follow_redirects=True
                    )
                    user = User.query.get(g.user)
                    assert ori_times_left == user.times_left
                    assert ori_guesses_len == len(user.cur_guesses)-1
                    assert ori_white_spaces > user.render.count('_')
                    break

    # guess new letter not in the word: 1 less guesses left; 1 more len(guesses); same in render
    def test_guess_wrong_letter(self):
        with app.test_client(self) as tester:
            tester.get(
                '/login',
                data=dict(username='test'),
                follow_redirects=True
            )
            tester.get('/play', follow_redirects=True)
            user = User.query.get(g.user)
            ori_times_left = user.times_left
            ori_guesses = user.cur_guesses
            ori_guesses_len = len(ori_guesses)
            ori_white_spaces = user.render.count('_')
            for char in "zxcvbqpoieawuyrtmnblkjhgfds".upper():
                if char not in user.cur_word and char not in ori_guesses:
                    response = tester.post(
                        '/play/'+str(g.user),
                        data=dict(letter=char),
                        follow_redirects=True
                    )
                    user = User.query.get(g.user)
                    assert ori_times_left-1 == user.times_left
                    assert ori_guesses_len == len(user.cur_guesses)-1
                    assert ori_white_spaces == user.render.count('_')
                    break

    # guess already guessed letter / non alphabetical letter: same response
    def test_guess_already_guessed_letter(self):
        with app.test_client(self) as tester:
            tester.get(
                '/login',
                data=dict(username='test'),
                follow_redirects=True
            )
            tester.get('/play', follow_redirects=True)
            response = tester.post(
                '/play/'+str(g.user),
                data=dict(letter='Z'),
                follow_redirects=True
            )
            response2 = tester.post(
                '/play/'+str(g.user),
                data=dict(letter='Z'),
                follow_redirects=True
            )
            response3 = tester.post(
                '/play/'+str(g.user),
                data=dict(letter='1'),
                follow_redirects=True
            )
            assert response.data == response2.data
            assert response.data == response3.data


    ## Test scoreboard

    # win
    def test_win_score(self):
        with app.test_client(self) as tester:
            tester.get(
                '/login',
                data=dict(username='test'),
                follow_redirects=True
            )
            tester.get('/play', follow_redirects=True)
            user = User.query.get(g.user)
            ori_wins = user.wins
            for char in user.cur_word:
                response = tester.post(
                    '/play/'+str(g.user),
                    data=dict(letter=char),
                    follow_redirects=True
                )
            user = User.query.get(g.user)
            assert user.wins == ori_wins+1

    # lose
    def test_lose_score(self):
        with app.test_client(self) as tester:
            tester.get(
                '/login',
                data=dict(username='test'),
                follow_redirects=True
            )
            tester.get('/play', follow_redirects=True)
            user = User.query.get(g.user)
            ori_loses = user.loses
            ori_guesses = user.cur_guesses
            count = 0
            for char in "zxcvbqpoieawuyrtmnblkjhgfds".upper():
                if count >= 9: break
                if char not in user.cur_word and char not in ori_guesses:
                    response = tester.post(
                        '/play/'+str(g.user),
                        data=dict(letter=char),
                        follow_redirects=True
                    )
                    count+=1
            user = User.query.get(g.user)
            assert user.loses == ori_loses+1

if __name__ == "__main__":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db.drop_all()
    db.create_all()
    unittest.main()