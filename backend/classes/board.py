#! /bin/python3

from pieces import *
from fen import *

class Board():
    #Rank = line, file = column
    conversion = dict(zip("abcdefgh", [0, 1, 2, 3, 4, 5, 6, 7]))
    invert = {values: keys for keys, values in conversion.items()}

    def __init__(self, fen_str="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        fen = Fen_String(fen_str)
        self.board = fen.board
        self.info = fen.info

    def __str__(self):
        string = str()
        for rank in self.board:
            string += str(rank) + "\n"
        return string
    
    def move(self, move):
        o_rank, o_file = Board.tile_to_index(move[:2])
        t_rank, t_file = Board.tile_to_index(move[2:])
        print((o_rank, o_file), (t_rank, t_file))
        if move in self.get_legal_moves():
            self.board[t_rank][t_file] = self.board[o_rank][o_file]
            self.board[o_rank][o_file] = No_Piece()

    def get_legal_moves(self):
        legal_moves = list()
        for rank in range(8):
            for file in range(8):
                if not isinstance(self.board[rank][file], No_Piece):
                    position = (rank, file)
                    possible_moves = self.board[rank][file].generate_moves(self, position)
                    for move in possible_moves:
                        legal_moves.append(str(Board.index_to_tile(position)) + str(Board.index_to_tile(move)))
        return legal_moves

    def non_empty_indexes(self):
        ls = list()
        for rank in range(8):
            for file in range(8):
                if not isinstance(self.board[rank][file], No_Piece):
                    ls.append((rank, file))
        return ls


    @staticmethod
    def tile_to_index(tile):
        file = Board.conversion[tile[0]]
        rank = abs(int(tile[1])-8)
        return (rank, file)

    @staticmethod
    def index_to_tile(index):
        rank = str(abs(index[0]-8))
        file = Board.invert[index[1]]
        return file + rank
        

if __name__ == "__main__":
    a = Board()
    print(a)
    print(a.info)
    b = a.get_legal_moves()
    print(b, len(b), "\n")

    ex = "r4rk1/pppq1p1p/2n1pnp1/3p1b2/3P4/2NBPN2/PPPQ1PPP/R3K2R w KQ - 0 1"
    assert Fen_String.encryptFen(a)
    a = Board(ex)
    print(a)
    print(a.info)
    b = a.get_legal_moves()
    print(b, len(b))

    a.move("a2a4")
    print(a)
    b = a.get_legal_moves()
    print(b, len(b))
