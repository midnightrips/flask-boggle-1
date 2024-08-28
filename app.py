from boggle import Boggle
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '12345'
app.debug = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def show_board():
    """Creates and shows boggle board"""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    plays = session.get('plays', 0)
    return render_template('board.html', board=board, highscore=highscore, plays=plays)


@app.route('/guess')
def valid_word(): #checks if word exists and returns JSON
    """Checks if word exists and returns JSON"""
    
    guess = request.args['guess']
    board = session.get('board')

    if not board:
        print("Board not found in session. Initializing new board.")
        board = boggle_game.make_board()
        session['board'] = board

    result = boggle_game.check_valid_word(board, guess)

    return jsonify({'result': result})

@app.route('/score', methods=['POST', 'GET'])
def post_score():
    
    print(request.json)
    score = request.json['score']
    print(score)
    highscore = session.get('highscore', 0)
    plays = session.get('plays', 0)

    session['highscore'] = max(score, highscore)
    session['plays'] = plays + 1
    return jsonify(highscore)
