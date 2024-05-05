#! /bin/python3
"""Initial tests. These tests may no longer be valid anymore since the class was modified a lot since then."""

import sys
sys.path.insert(1, './classes')

import requests
from pieces import *

BASE = "http://127.0.0.1:5000/"

class Matrix():
    def __init__(self, string):
        """Initializes a board matrix using a FEN string"""

        temp = string.split()
        temp_board = temp[0].split("/")
        self.board = list()
        for rank in range(len(temp_board)):
            line = list()
            file = 0
            while file < len(temp_board[rank]):
                try:
                    num = int(temp_board[rank][file])
                    line.extend([No_Piece()]*num)
                    temp_board[rank] = temp_board[rank][:file] + "."*num + temp_board[rank][file+1:]
                    file += num
                except ValueError:
                    piece_name = temp_board[rank][file]
                    piece = Piece.translate(piece_name)
                    line.append(piece)
                    file += 1
            self.board.append(line)

    def __repr__(self):
        string = str()
        for rank in self.board:
            string += str(rank) + "\n"
        return string


initialize = {"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"}
data = [{'move': "d2d4"}, {'move': "e7e6"}, {'move': "d4d5"}, {'move': "c7c5"}, {'move': "d5c6"}]

response = requests.post(BASE + "/create", json=initialize)
print(response.json())

for inp in data:
    response = requests.post(BASE + "/move", json=inp)
    response = response.json()
    print(response)
    print(Matrix(response["board"]))
