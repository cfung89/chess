#! /bin/python3

from board import *
from pieces import *
from bot import *
from squares import *

class Game():
    def __init__(self, fen):
        self.board = Board(fen_str=fen)
        self.turn = self.board.get_info()["side"]
        self.legal_moves = self.board.get_legal_moves(self.turn)

    def move(self, move):
        self.board.move(move)
    
    def bot(self):
        #move = evaluate_random(self.legal_moves)
        move, eval = evaluate_game(self.board, 2, -float('inf'), float('inf'), True)
        orig = Square.tile_to_index(move[:2])
        new = list(Square.tile_to_index(move[2:]))
        if type(self.board.board[orig[0]][orig[1]]) == King:
            if new[1] - orig[1] == 2:
                new[1] = 7
                move = move[:2] + Square.index_to_tile(new)
            elif new[1] - orig[1] == -2:
                new[1] = 0
                move = move[:2] + Square.index_to_tile(new)
        return move
    
    def game_over(self, repetition):
        return self.board.game_over(repetition)

    def game_info(self):
        new_fen = Fen_String.encryptFen(self.board)
        fen_board = new_fen.split()[0]

        info = self.board.get_info()
        player = info['side']
        castling = info['castling']
        en_passant = info['en_passant']

        response = {'board': fen_board, 'legal_moves': self.legal_moves}
        return new_fen, [fen_board, player, castling, en_passant], self.legal_moves, response
