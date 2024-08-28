from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        app.config['TESTING'] = True

    def test_show_board(self):
        with app.test_client() as client:
            
            res = client.get('/')

            self.assertEqual(res.status_code, 200)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('plays'))
    
    def test_valid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['G', 'U', 'E', 'S', 'S'],
                                           ['G', 'U', 'E', 'S', 'S'],
                                           ['G', 'U', 'E', 'S', 'S'],
                                           ['G', 'U', 'E', 'S', 'S'],
                                           ['G', 'U', 'E', 'S', 'S']]
            res = client.get('/guess?guess=guess')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['result'], 'ok')

    def test_invalid_word(self):
        with app.test_client() as client:
            res = client.get('/guess?guess=test')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['result'], 'not-on-board')

    def test_not_word(self):
        with app.test_client() as client:
            res = client.get('/guess?guess=abcd')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['result'], 'not-word')