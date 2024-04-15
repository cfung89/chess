#! /bin/python3

from pieces import *
from fen import *

def func(fen_str="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    fen = Fen_String(fen_str)
    board = fen.board
    info = fen.info
    return board, info

print(Piece.translate("q"))
