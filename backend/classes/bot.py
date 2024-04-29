#! /bin/python3

import requests
from game import *
from squares import *
from random import randint

class Bot():
    def __init__(self, colour):
        self.colour = colour

    def evaluate_opening(self, fen):
        pass

    def evaluate_middlegame(self, board, moves):
        o_pos = list(moves.keys())
        chosen_pos = o_pos[randint(0, len(o_pos)-1)]
        while not moves[chosen_pos]:
            chosen_pos = o_pos[randint(0, len(o_pos)-1)]
        chosen_move = moves[chosen_pos][randint(0, len(moves[chosen_pos])-1)]
        return Square.index_to_tile(chosen_pos) + Square.index_to_tile(chosen_move)

    def evaluate(self, board, moves):
        pass

    def evaluate_endgame(self):
        pass

if __name__ == "__main__":
    from board import *
    from fen import *

    ex = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    a = Board(fen_str=ex)
    #a.move("d2d4")
    #a.move("e7e6")
    b = Bot(0)
    colour = 1

    for loop in range(30):
        white, black, w_boards, b_boards = a.get_legal_moves()
        new = b.evaluate_middlegame(a, white if colour else black)
        a.move(new)
        print(a)
        colour = 0 if colour else 1
