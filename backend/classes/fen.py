#! /bin/python3

from pieces import *

class Fen_String():
    """FEN string class"""

    def __init__(self, string):
        """Initializes a board matrix using a FEN string"""

        temp = string.split()
        temp_board, temp_info = temp[0].split("/"), temp[1:]
        self.board = list()
        coords = dict()
        for rank in range(len(temp_board)):
            line = list()
            file = 0
            while file < len(temp_board[rank]):
                try:
                    num = int(temp_board[rank][file])
                    line.extend([No_Piece()]*num)
                    temp_board[rank] = temp_board[rank][:file] + "."*num + temp_board[rank][file+1:]
                    file += num
                except ValueError:
                    piece_name = temp_board[rank][file]
                    piece = Piece.translate(piece_name)
                    line.append(piece)
                    if type(piece) == King:
                        coords[piece.colour] = (rank, file)
                    file += 1
            self.board.append(line)
        self.info = {"side": WHITE if temp_info[0] == "w" else BLACK, "castling": temp_info[1], "en_passant": temp_info[2], "halfmove": int(temp_info[3]), "fullmove": int(temp_info[4])}
        self.king_pos = coords

    def __repr__(self):
        string = str()
        for rank in self.board:
            string += str(rank) + "\n"
        return string

    @staticmethod
    def encryptFen(board_obj):
        """Transforms a board state back into a FEN string."""

        board, info = board_obj.board, board_obj.info
        fen_string = str()
        for rank in board:
            num = 0
            for piece_name in rank:
                if type(piece_name) == No_Piece:
                    num += 1
                else:
                    if num:
                        fen_string += str(num)
                        num = 0
                    fen_string += piece_name.name
            if num:
                fen_string += str(num)
                num = 0
            fen_string += "/"
        fen_string = fen_string[:-1]
        information = list(info.values())
        fen_string += " w" if information[0] else " b"
        for i in information[1:]:
            fen_string += " " + str(i)
        return fen_string


if __name__ == "__main__":
    #Testing code
    a = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    print(a)
    board = Fen_String(a)
    print(board)
    print(board.info)
    b = Fen_String.encryptFen(board)
    print(b, "\n")
    assert a == b

    a = "r4rk1/pppq1p1p/2n1pnp1/3p1b2/3P4/2NBPN2/PPPQ1PPP/R3K2R w KQ - 0 1"
    print(a)
    board = Fen_String(a)
    print(board)
    print(board.info)
    b = Fen_String.encryptFen(board)
    print(b, "\n")
    assert a == b
