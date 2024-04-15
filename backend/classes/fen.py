#! /bin/python3

from pieces import *

class Fen_String():
    def __init__(self, string):
        temp = string.split()
        temp_board, temp_info = temp[0].split("/"), temp[1:]
        self.board = list()
        for rank in temp_board:
            line = list()
            for piece_name in rank:
                try:
                    num = int(piece_name)
                    line.extend([No_Piece()]*num)
                    continue
                except ValueError:
                    line.append(Piece.translate(piece_name))
            self.board.append(line)
        self.info = {"side": WHITE if temp_info[0] == "w" else BLACK, "castling": temp_info[1], "en_passant": temp_info[2], "halfmove": int(temp_info[3]), "fullmove": int(temp_info[4])}

    @staticmethod
    def encryptFen(board_obj):
        board, info = board_obj.board, board_obj.info
        fen_string = str()
        for rank in board:
            num = 0
            for piece_name in rank:
                if piece_name == ".":
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
        info = list(info.values())
        fen_string += " w" if info[0] else " b"
        for i in info[1:]:
            fen_string += " " + str(i)
        return fen_string


if __name__ == "__main__":
    a = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = Fen_String(a)
    print(board.board)
    print(board.info)
    b = Fen_String.encryptFen(board.board, board.info)
    print(b)
    assert a == b
