#! /bin/python3

from board import *
from pieces import *
from bot import *

WHITE = 1
BLACK = 0

class Game():
    def __init__(self, fen):
        self.board = Board(fen_str=fen)
        self.update_moves()

    def update_moves(self):
        white, black, w_boards, b_boards = self.board.get_legal_moves()
        turn = self.board.get_info()["side"]
        colours = {WHITE: white, BLACK: black}
        self.legal_moves = colours[turn]
        king = self.board.get_king_position()[turn]
        return king, turn, colours

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
    
    def bot(self):
        move = evaluate_random(self.board, self.legal_moves)
        return move


    def game_over(self, repetition):
        if len(repetition) >= 3:
            return 4        #draw by repetition
        
        king, turn, colours = self.update_moves()
        moves = self.get_moves()

        if self.board.isChecked(king, colours, colours[Game.get_opponent(turn)]):
            if moves:       #change the condition
                return 0        #Only check
            else:
                return 1        #checkmate
        elif not moves:
            return 2        #stalemate

        if self.board.info["halfmove"] >= 100:        #and side to move has at least one legal move
            return 3    #50-move draw
        return 0

    def game_info(self):
        new_fen = Fen_String.encryptFen(self.board)
        fen_board = new_fen.split()[0]

        info = self.board.get_info()
        player = info['side']
        castling = info['castling']
        en_passant = info['en_passant']

        legal_moves = {str(pos): self.legal_moves[pos] for pos in self.legal_moves}
        response = {'board': fen_board, 'legal_moves': legal_moves}
        return new_fen, [fen_board, player, castling, en_passant], legal_moves, response
