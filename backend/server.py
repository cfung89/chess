from flask import Flask, request, jsonify, Response
from flask_cors import CORS

import time
import sys
sys.path.insert(1, './classes')

from game import *
from fen import Fen_String
from pymongo import MongoClient


app = Flask(__name__)       #Creates a Flask app
CORS(app)       #Applies Cross-Origin Resource Sharing (CORS) to the app.

client = MongoClient("localhost", 27017)        #Connects to MongoDB database with Python

db = client.chessdb
gamelog = db.gamelog
db.drop_collection('gamelog')

@app.route('/create', methods=['POST'])
def new_game():
    """Creates/initializes a new game. Gets the FEN string as a message."""
    db.drop_collection('gamelog')
    resp = request.get_json()
    game = Game(resp['fen'])

    new_fen, info, legal_moves, response = game.game_info()
    gamelog.insert_one({"fen": new_fen, "info": info, "moves": legal_moves})        #Adds the first, initial board to the database
    response['result'] = game.game_over([b for b in gamelog.find({"info": info})])
    response = jsonify(response)
    return response, 200

@app.route('/move', methods=['POST'])
def board_move():
    """Makes a move, by adding it to the database. Gets the the string of the move."""
    resp = request.get_json()
    last = gamelog.find().sort({"_id":-1}).limit(1)     #Gets the last move in the database
    fen = [entry for entry in last][0]["fen"]
    game = Game(fen)
    game.move(resp['move'])

    with open("boards.txt", "a") as fp:     #Saves the board to a txt file (for testing purposes only)
        print(game.board, file=fp)

    new_fen, info, legal_moves, response = game.game_info()

    gamelog.insert_one({"fen": new_fen, "info": info, "moves": legal_moves})
    response['result'] = game.game_over([b for b in gamelog.find({"info": info})])      #Returns the state of the game (if it is the end). The parameter of the function is a list of the repetitions of the last move
    if response["result"]:
        db.drop_collection('gamelog')
    response = jsonify(response)
    return response, 200

@app.route('/botmove', methods=['GET'])
def bot_move():
    """Returns the move calculated by the bot"""
    time.sleep(0.1)     #Short time delay to ensure that the bot gets the latest move.
    last = gamelog.find().sort({"_id":-1}).limit(1)     #Gets the last move in the database
    fen = [entry for entry in last][0]["fen"]
    game = Game(fen)
    botmove = game.bot()
    if botmove != "":
        move = {"move": botmove} 
        return jsonify(move), 200
    else:
        db.drop_collection('gamelog')
        return Response(status=204)

@app.route('/legalmoves', methods=['GET'])
def piece_move():
    time.sleep(0.1)
    last = gamelog.find().sort({"_id":-1}).limit(1)
    legal_moves = [entry for entry in last][0]["moves"]
    return jsonify(legal_moves), 200


@app.route('/resign', methods=['POST'])
def resign():
    db.drop_collection('gamelog')

if __name__ == "__main__":
    app.run(debug=True)
