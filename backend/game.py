#! /bin/python3

from board import *
from pieces import *

class Game():
    def __init__(self, fen, user_colour):
        self.human = user_colour
        self.computer = 0 if user_colour else 1
        self.board = Board(fen=fen)

    def game_over(self):
        turn = self.board.info["side"]
        white, black = self.board.get_legal_moves()
        colours = {WHITE: white, BLACK: black}
        king_pos = self.board.get_king_position()
        if not Board.get_moves(colours[turn]):
            return 2        #stalemate
        for colour in colours:
            moves = colours[colour]
            opp = Game.get_moves(colour)
            if self.board.isChecked(colour, colours[opp]):
                if not moves:       #change the condition
                    return 0        #Only check
                else:
                    return 1        #checkmate
        if self.info["halfmove"] >= 100:        #and side to move has at least one legal move
            return 3    #50-move draw
        if self.repetition():
            return 4
        return False

    def move(self, move):
        self.board.move(move)
        return self.board.board

    def repetition(self):
        pass

    @staticmethod
    def get_opponent(player):
        if player == self.human:
            return self.computer
        return self.human
