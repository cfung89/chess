#! /bin/python3

from board import *
from pieces import *
from bot import *
from squares import *

class Game():
    """Game class"""

    def __init__(self, fen):
        self.board = Board(fen_str=fen)
        self.turn = self.board.get_info()["side"]
        self.legal_moves = self.board.get_legal_moves(self.turn)

    def move(self, move):
        """Makes a move on the board"""
        self.board.move(move)
    
    def bot(self):
        """Gets the bot's best calculated move"""
        #move = evaluate_random(self.legal_moves)
        move, eval = evaluate_game(self.board, 2, -float('inf'), float('inf'), True)        #Evaluates the board and returns the best move for the bot
        
        #Checks if the bot chose a castling move. We have to convert the squares for the frontend.
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
        """Returns the state of the game (if it is over)"""
        return self.board.game_over(repetition)

    def game_info(self):
        """Gets certain information of the board and the game, for the server to send back to the frontend."""
        new_fen = Fen_String.encryptFen(self.board)
        fen_board = new_fen.split()[0]

        info = self.board.get_info()
        player = info['side']
        castling = info['castling']
        en_passant = info['en_passant']

        response = {'board': fen_board, 'legal_moves': self.legal_moves}
        return new_fen, [fen_board, player, castling, en_passant], self.legal_moves, response
