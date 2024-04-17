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
        self.timeline = list()

    def __repr__(self):
        string = str()
        for rank in self.board:
            string += str(rank) + "\n"
        return string
    
    def get_info(self):
        fen_info = self.info.copy()
        fen_info.pop("king_position")
        return fen_info

    def get_king_position(self):
        return self.info["king_position"]

    def move(self, move):
        o_rank, o_file = Board.tile_to_index(move[:2])
        t_rank, t_file = Board.tile_to_index(move[2:])
        piece = self.board[o_rank][o_file]
        capture = self.board[t_rank][t_file]

        if move in self.get_legal_moves():
            if type(piece) == Pawn:
                if (o_rank == 1 or o_rank == 6) and (t_rank == 3 or t_rank == 4):
                    self.info["en_passant"] = move[2:]
                else:
                    self.info["en_passant"] = "-"
            elif type(piece) == King:
                if self.info["castling"] != "-":
                    if str(piece) in self.info["castling"]:
                        if str(piece).isupper():
                            self.info["castling"] = self.info["castling"][2:]
                        else:
                            self.info["castling"] = self.info["castling"][:2]
                    if not self.info["castling"]:
                        self.info["castling"] = "-"
            
            if capture != No_Piece or type(piece) == Pawn:
                self.info["halfmove"] = 0
            else:
                self.info["halfmove"] += 1

            if piece.colour == BLACK:
                self.info["fullmove"] += 1

            self.info["side"] = BLACK if self.info["side"] == WHITE else WHITE

            self.board[t_rank][t_file] = self.board[o_rank][o_file]
            self.board[o_rank][o_file] = No_Piece()

        else:
            raise ValueError("Invalid move")

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
    
    def check(self, king_pos, attacked):
        for colour in king_pos:
            if colour in attacked:
                return colour
        return None

    def game_over(self):
        king_pos = self.get_king_position()
        attacked = self.attacked_squares()
        isChecked = self.check(king_pos, attacked)
        if isChecked is not None:
            if not self.board[king_pos[0]][king_pos[1]].generate_moves(self, position):
                return Game.get_opponent(isChecked)
        if not self.get_legal_moves():
            return 2        #stalemate
        if self.info["halfmove"] >= 100:        #and side to move has at least one legal move
            return 3    #50-move draw
        return False


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
    print("En passant test")
    a.move("d2d4")
    a.move("e7e6")
    a.move("d4d5")
    a.move("c7c5")
    print(a)
    print(a.info)
    b = a.get_legal_moves()
    print(b, len(b), "\n")

    ex = "r4rk1/pppq1p1p/2n1pnp1/3p1b2/3P4/2NBPN2/PPPQ1PPP/R3K2R w KQ - 0 1"
    a = Board(ex)
    assert Fen_String.encryptFen(a) == ex
    print(a)
    print(a.info)
    b = a.get_legal_moves()
    print(b, len(b))

    a.move("a2a4")
    print(a)
    b = a.get_legal_moves()
    print(b, len(b))
