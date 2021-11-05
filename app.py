from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route("/board")
def show_board():
    board_game = boggle_game.make_board()
    session["board"] = board_game
    highscore = session.get("highscore", 0)
    # why session["numOfPlay"] = 0 won't work?
    numOfPlay = session.get("numOfPlay", 0)
    return render_template("/board.html",
    board = session["board"],
    number=highscore, times=numOfPlay,
    score=0, seconds=60)


@app.route("/check-word")
def check_word():
    word = request.args["word"]
    board = session.get("board")
    result = boggle_game.check_valid_word(board, word)
    return result


@app.route("/post-score", methods=["POST"])
def find_high_score():
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