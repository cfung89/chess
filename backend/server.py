from flask import Flask, request, jsonify, Response
from flask_cors import CORS

import time
import sys
sys.path.insert(1, './classes')

from game import *
from fen import Fen_String
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)

client = MongoClient("localhost", 27017)

db = client.chessdb
gamelog = db.gamelog
db.drop_collection('gamelog')

@app.route('/create', methods=['POST'])
def new_game():
    db.drop_collection('gamelog')
    resp = request.get_json()
    game = Game(resp['fen'])

    new_fen, info, legal_moves, response = game.game_info()
    gamelog.insert_one({"fen": new_fen, "info": info, "moves": legal_moves})
    response['result'] = game.game_over([b for b in gamelog.find({"info": info})])
    response = jsonify(response)
    return response, 200

@app.route('/move', methods=['POST'])
def board_move():
    resp = request.get_json()
    last = gamelog.find().sort({"_id":-1}).limit(1)
    fen = [entry for entry in last][0]["fen"]
    game = Game(fen)
    game.move(resp['move'])
    with open("boards.txt", "a") as fp:
        print(game.board, file=fp)

    new_fen, info, legal_moves, response = game.game_info()

    gamelog.insert_one({"fen": new_fen, "info": info, "moves": legal_moves})
    response['result'] = game.game_over([b for b in gamelog.find({"info": info})])
    if response["result"]:
        db.drop_collection('gamelog')
    response = jsonify(response)
    return response, 200

@app.route('/botmove', methods=['GET'])
def bot_move():
    last = gamelog.find().sort({"_id":-1}).limit(1)
    fen = [entry for entry in last][0]["fen"]
    game = Game(fen)
    botmove = game.bot()
    if botmove is not None:
        move = {"move": botmove} 
    else:
        db.drop_collection('gamelog')
        return Response(status=204)
    new_fen, info, legal_moves, response = game.game_info()

    #gamelog.insert_one({"fen": new_fen, "info": info, "moves": legal_moves})
    #result = game.game_over([b for b in gamelog.find({"info": info})])
    #if result:
    #    db.drop_collection('gamelog')
    return jsonify(move), 200

@app.route('/legalmoves', methods=['GET'])
def piece_move():
    try:
        last = gamelog.find().sort({"_id":-1}).limit(1)
        legal_moves = [entry for entry in last][0]["moves"]
    except IndexError:
        game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        king, turn, colours = game.update_moves()
        legal_moves = colours[0]|colours[1]
        legal_moves = {str(pos): legal_moves[pos] for pos in legal_moves}
    return jsonify(legal_moves), 200


@app.route('/resign', methods=['POST'])
def resign():
    db.drop_collection('gamelog')

if __name__ == "__main__":
    app.run(debug=True)
