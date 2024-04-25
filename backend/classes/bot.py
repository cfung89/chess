#! /bin/python3

import requests
from game import *

class Bot():
    def __init__(self, colour):
        self.colour = colour

    def evaluate_opening(self, fen):
        pass

    def evaluate_middlegame(self):
        pass

    def evaluate_endgame(self):
        pass

if __name__ == "__main__":
    from board import *
    from fen import *

    ex = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    a = Board(fen_str=ex)
    a.move("d2d4")
    a.move("e7e6")
    b = Bot(0)

    for loop in range(30):
        fen = Fen_String.encryptFen(a)
        new = b.evaluate_opening(fen)
        a.move(new)
