from unittest import TestCase
from app import app
from flask import session, jsonify
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_board_page(self):
        """test initial page"""
        with self.client as client:
            response = client.get('/board')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('numOfPlay'))
            self.assertIn(b'Score:', response.data)
            print(response.data)
            self.assertIn(b'Seconds Left:', response.data)
            self.assertIn(b'High Score:', response.data)

    def test_valid_word(self):
        """test if word valid return ok msg"""
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [
                    ['W', 'B', 'Y', 'T', 'D'],
                    ['Q', 'X', 'X', 'O', 'R'],
                    ['U', 'X', 'X', 'N', 'X'],
                    ['D', 'W', 'L', 'K', 'Q'],
                    ['L', 'F', 'W', 'T', 'N']
                ]
        
        response = self.client.get('/check-word?word=to')
        # without b'ok' it shows [wrappertst response streamed[200 ok]? 
        # How to make response.data = ok here?
        # I tried to use jsonify here, but does not work.
        self.assertEqual(response.data, b'ok')

    def test_not_valid_word(self):
        """test if not valid word return not-word"""
        self.client.get('/board')
        response = self.client.get('/check-word?word=telephone')
        self.assertEqual(response.data, b'not-on-board')   

    def test_not_a_word(self):
        """test if not a word return not-word"""
        self.client.get('/board')
        response = self.client.get('/check-word?word=oa')
        self.assertEqual(response.data, b'not-word')    

