#! /bin/python3

from board import *
from pieces import *
from bot import *

class Game():
    def __init__(self, fen):
        self.board = Board(fen_str=fen)
        self.turn = self.board.get_info()["side"]
        self.legal_moves = self.board.get_legal_moves(self.turn)

    def move(self, move):
        self.board.move(move)
    
    def bot(self):
        #move = evaluate_random(self.legal_moves)
        move, eval = evaluate_game(self.board, 2, -float('inf'), float('inf'), True, 0)
        print("FINAL MOVE", move, eval)
        return move

    def game_over(self, repetition):
        if len(repetition) >= 3:
            print("repetition")
            return 4        #draw by repetition
        
        king = self.board.get_king_position()[self.turn]

        if self.board.isChecked(king, self.board.get_attacking_moves(0 if self.turn else 1)):
            if not self.legal_moves:       #change the condition
                print("checkmate")
                return 1        #checkmate
            else:
                print("check")
                return 0
        elif not self.legal_moves:
            print("stalemate")
            return 2        #stalemate

        if self.board.info["halfmove"] >= 100:        #and side to move has at least one legal move
            print("draw")
            return 3    #50-move draw
        print("nothing")
        return 0

    def game_info(self):
        new_fen = Fen_String.encryptFen(self.board)
        fen_board = new_fen.split()[0]

        info = self.board.get_info()
        player = info['side']
        castling = info['castling']
        en_passant = info['en_passant']

        response = {'board': fen_board, 'legal_moves': self.legal_moves}
        return new_fen, [fen_board, player, castling, en_passant], self.legal_moves, response
