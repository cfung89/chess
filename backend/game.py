#! /bin/python3

from board import *
from pieces import *

class Game():
    def __init__(self, fen, user_colour):
        self.human = user_colour
        self.computer = 0 if user_colour else 1
        self.board = Board(fen=fen)
        self.legal_moves

    def get_moves(self):
        moves = list()
        for loop in self.legal_moves.values():
            moves.extend(loop)
        return moves

    @staticmethod
    def get_opponent(colour):
        if colour:
            return 0
        return 1

    def move(self, move):
        self.board.move(move)
        return self.board.board

    def game_over(self, repetition):
        if repetition >= 3:
            return 4        #draw by repetition
        
        white, black, w_boards, b_boards = self.board.get_legal_moves()
        king_pos = self.board.get_king_position()

        turn = self.board.get_info()["side"]
        colours = {WHITE: white, BLACK: black}

        self.legal_moves = colours[turn]
        moves = self.get_moves()

        if self.board.isChecked(colour, colours[Game.get_opponent(turn)]):
            if moves:       #change the condition
                return 0        #Only check
            else:
                return 1        #checkmate
        elif not moves:
            return 2        #stalemate

        if self.info["halfmove"] >= 100:        #and side to move has at least one legal move
            return 3    #50-move draw
        return 0
