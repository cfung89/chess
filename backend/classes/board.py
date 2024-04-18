#! /bin/python3

from pieces import *
from fen import *
from squares import *

class Board():
    #Rank = line, file = column
    conversion = dict(zip("abcdefgh", [0, 1, 2, 3, 4, 5, 6, 7]))
    invert = {values: keys for keys, values in conversion.items()}

    def __init__(self, board=None, info=None, king_pos=None, fen_str=None):

        self.board = board
        self.info = info
        self.king_pos = king_pos
        
        if fen_str:
            fen = Fen_String(fen_str)
            self.board = fen.board
            self.info = fen.info
            self.king_pos = fen.king_pos

        if self.board is None:
            raise ValueError("Cannot create Board instance without information.")

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
        return self.king_pos

    def board_copy(self):
        return [[value for value in i] for i in self.board]

    def move(self, move):
        def _move(copy_board, o_rank, o_file, t_rank, t_file):
            piece = copy_board[o_rank][o_file]
            copy_board[t_rank][t_file] = copy_board[o_rank][o_file]
            copy_board[o_rank][o_file] = No_Piece()
            king_pos = (o_rank, o_file)
            if type(piece) == Pawn and Square.index_to_tile((o_rank, t_file)) == self.info["en_passant"]:
                copy_board[o_rank][t_file] = No_Piece()
            elif type(piece) == King:
                king_pos = (t_rank, t_file)
                if t_file - o_file == 2:
                    rook_pos = len(copy_board)[t_rank]-1
                    rook = copy_board[t_rank][rook_pos]
                    assert type(rook) == Rook
                    while type(copy_board[t_rank][rook_pos]) != King:
                        rook_pos -= 1
                    copy_board[t_rank][rook_pos-1] = copy_board[t_rank][len(copy_board)[t_rank]-1]
                    copy_board[t_rank][len(copy_board)[t_rank]-1] = No_Piece()
            return copy_board, king_pos

        o_rank, o_file = Square.tile_to_index(move[:2])
        t_rank, t_file = Square.tile_to_index(move[2:])
        white, black = self.get_legal_moves()
        piece = self.board[o_rank][o_file]
        capture = self.board[t_rank][t_file]
        piece_moves = white if piece.colour else black

        temp = None
        if (t_rank, t_file) in piece_moves[(o_rank, o_file)]:
            temp, king_pos = _move(self.board_copy(), o_rank, o_file, t_rank, t_file)
            temp_board = Board(board=temp, king_pos=king_pos)
        else:
            raise ValueError()
            return False
        if temp_board.isChecked(piece.colour, black if piece.colour else white):
            raise ValueError()
            return False

        self.info["side"] = BLACK if self.info["side"] else WHITE
        if type(piece) == Pawn:
            if t_rank - o_rank == 2:
                self.info["en_passant"] = move[2:]
            else:
                self.info["en_passant"] = "-"
        elif type(piece) == King:
            if self.info["castling"] != "-":
                if str(piece) in self.info["castling"]:
                    if str(piece).isupper():
                        self.info["castling"].replace("KQ", "")
                    else:
                        self.info["castling"].replace("kq", "")
                if not self.info["castling"]:
                    self.info["castling"] = "-"
            self.king_pos[piece.colour] = (t_rank, t_file)
        elif type(piece) == Rook:
            if self.info["castling"] != "-":
                if str(piece) in self.info["castling"]:
                    if str(piece).isupper() and o_file >= 4:
                        self.info["castling"].replace("K", "")
                    if str(piece).isupper() and o_file <= 3:
                        self.info["castling"].replace("Q", "")
                    if str(piece).islower() and o_file >= 4:
                        self.info["castling"].replace("k", "")
                    else:
                        self.info["castling"].replace("q", "")
                if not self.info["castling"]:
                    self.info["castling"] = "-"
            
            if capture != No_Piece or type(piece) == Pawn:
                self.info["halfmove"] = 0
            else:
                self.info["halfmove"] += 1

            if piece.colour == BLACK:
                self.info["fullmove"] += 1
            
        self.board = temp
        return True

    def get_legal_moves(self):
        white = dict()
        black = dict()
        for rank in range(len(self.board)):
            for file in range(len(self.board[rank])):
                piece = self.board[rank][file]
                if type(piece) != No_Piece:
                    position = (rank, file)
                    possible_moves = piece.generate_moves(self, position)
                    if piece.colour:
                        white[position] = possible_moves
                    else:
                        black[position] = possible_moves
        white, black = self.castling(white, black)
        for colour in self.get_king_position():
            legal_moves = white if colour else black
            opponent_moves = black if colour else white
            pos = self.get_king_position()[colour]

            king_moves = set(legal_moves.pop(pos))
            temp = set(Board.get_moves(opponent_moves))
            king_moves = list(king_moves - temp)
            legal_moves[pos] = king_moves
        return white, black

    @staticmethod
    def get_moves(legal_moves):
        temp = list()
        for loop in legal_moves.values():
            temp.extend(loop)
        return temp

    def castling(self, white, black):
        board = self.board
        castle_info = self.info["castling"]
        for colour in (WHITE, BLACK):
            full = "KQ" if colour else "kq"
            king_x, king_y = self.get_king_position()[colour]
            for move in set(full).intersection(set(castle_info)):
                direction = 1 if move.lower() == "k" else -1
                rook_y = king_y + 1
                piece = board[king_x][rook_y]
                success = True
                while type(piece) != Rook:
                    if type(piece) == No_Piece:
                        rook_y += 1
                        piece = board[king_x][rook_y]
                    else:
                        success = False
                        break
                if success:
                    if colour:
                        white[(king_x, king_y)].append((king_x, rook_y-1 if direction == 1 else rook_y+2))
                    else:
                        black[(king_x, king_y)].append((king_x, rook_y-1 if direction == 1 else rook_y+2))
        return white, black

    def isChecked(self, colour, opp_moves):
        king = self.get_king_position()[colour]
        attacked = Board.get_moves(opp_moves)
        if king in attacked:
            return True
        return False

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


if __name__ == "__main__":
    ex = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    a = Board(fen_str=ex)
    print(a)
    print(a.info)
    b = a.get_legal_moves()
    print(b, "\n")
    print("En passant test")
    a.move("d2d4")
    a.move("e7e6")
    a.move("d4d5")
    a.move("c7c5")
    print(a)
    a.move("d5c6")
    print(a)
    print(a.info)
    b = a.get_legal_moves()
    print(b, "\n")
    print("End passant test")

    ex = "r4rk1/pppq1p1p/2n1pnp1/3p1b2/3P4/2NBPN2/PPPQ1PPP/R3K2R w KQ - 0 1"
    a = Board(fen_str=ex)
    assert Fen_String.encryptFen(a) == ex
    print(a)
    print(a.info)
    b = a.get_legal_moves()
    print(b)

    a.move("a2a4")
    print(a)
    b = a.get_legal_moves()
    print(b)
