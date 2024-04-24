from flask import Flask, request, jsonify
from flask_cors import CORS

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
    resp = request.get_json()
    game = Game(resp['fen'])

    new_fen, info, response = game.game_info()
    gamelog.insert_one({"fen": new_fen, "info": info})
    response['result'] = game.game_over([b for b in gamelog.find({"info": info})])
    response = jsonify(response)
    return response, 200

@app.route('/move', methods=['POST'])
def board_move():
    resp = request.get_json()
    print([i for i in gamelog.find()])
    last = gamelog.find().sort({"_id":-1}).limit(1)
    fen = [entry for entry in last][0]["fen"]
    game = Game(fen)
    game.move(resp['move'])

    new_fen, info, response = game.game_info()

    gamelog.insert_one({"fen": new_fen, "info": info})
    response['result'] = game.game_over([b for b in gamelog.find({"info": info})])
    if response["result"]:
        db.drop_collection('gamelog')
    response = jsonify(response)
    return response, 200

@app.route('/resign', methods=['POST'])
def resign():
    db.drop_collection('gamelog')

if __name__ == "__main__":
    app.run(debug=True)
