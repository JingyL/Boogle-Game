from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

boggle_game = Boggle()

@app.route("/board")
def show_board():
    """get information to show on board"""
    board_game = boggle_game.make_board()
    session["board"] = board_game
    # why session["numOfPlay"] = 0 won't work?
    # previous code I wrote:   it shows issue of Name Error, highscore is not defined
    # session["numOfPlay"] = 0
    # session["highscore"] = 0
    highscore = session.get("highscore", 0)
    numOfPlay = session.get("numOfPlay", 0)
    return render_template("/board.html",
    board = session["board"],
    number = highscore, times = numOfPlay,
    score = 0)


@app.route("/check-word")
def check_word():
    """get user word and check validity"""
    word = request.args["word"]
    board = session.get("board")
    result = boggle_game.check_valid_word(board, word)
    return result


@app.route("/post-score", methods=["POST"])
def find_high_score():
    """get score and compare to select the higher score"""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    if (highscore > score):
        session["highscore"] = highscore
    else:
        session["highscore"] = score
    highscore = session.get("highscore", 0)
    numOfPlay = session.get("numOfPlay", 0)
    session["numOfPlay"] = numOfPlay + 1

    return jsonify(highscore)