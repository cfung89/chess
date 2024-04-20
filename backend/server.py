from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import game
from fen import Fen_String


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gamelog.sqlite3"
#app.config["SQLALCHEMY_TRACK_MODIFICAITIONS"] = False
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class gamelog(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True, autoincrement=True)
    fen = db.Column(db.String(100))
    board = db.Column(db.String(100))
    player = db.Column(db.Integer)
    castling = db.Column(db.String(4))
    en_passant = db.Column(db.String(2))

    def __init__(self, fen, board, player, castling, en_passant):
        self.fen = fen
        self.board = board
        self.player = player
        self.castling = castling
        self.en_passant = en_passant

@app.route('/create', methods=['POST'])
def new_game():
    resp = request.get_json()
    game = Game(resp['fen'], resp['usr_colour'])

    fen_board = resp['fen'].split()[0]
    player = game.board.info['side']
    castling = game.board.info['castling']
    en_passant = game.board.info['en_passant']

    response = jsonify({'board': fen_board})
    db.session.add(gamelog(resp['fen'], fen_board, player, castling, en_passant))
    return response

@app.route('/move', methods=['POST'])
def board_move():
    resp = request.get_json()
    game = Game(gamelog.query.all()[-1].fen)
    game.move(resp['move'])

    new_fen = Fen_String.encryptFen(game.board)
    fen_board = new_fen.split()[0]
    player = game.board.info['side']
    castling = game.board.info['castling']
    en_passant = game.board.info['en_passant']

    repetition = gamelog.query.filter_by(board=fen_board, player=player, castling=castling, en_passant=en_passant).count()
    result = game.game_over(repetition)

    db.session.add(gamelog(new_fen, fen_board, player, castling, en_passant))
    db.commit()
    response = jsonify({'board': fen_board, 'legal_moves': game.legal_moves, 'result': result})
    return response, 200
    #return new_board, legal moves of new board, game_end? (or str to be interpreted by js code), 200


if __name__ == "__main__":
    app.run(debug=True)
