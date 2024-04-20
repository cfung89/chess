from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import game


app = Flask(__name__)
Cors(app)

@app.route('/create', methods=['POST'])
def new_game():
    response = request.get_json()
   pass 

@app.route('/resign', methods=['POST'])
def resign_game():
    response = request.get_json()
    pass
    #winner

@app.route('/move', methods=['POST'])
def board_move():
    response = request.get_json()
    pass
    #return new_board, legal moves of new board, game_end? (or str to be interpreted by js code), 200

if __name__ == "__main__":
    app.run(debug=True)
