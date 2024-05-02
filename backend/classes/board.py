#! /bin/python3

from copy import deepcopy
from pieces import *
from fen import *
from squares import *

class Board():
    #Rank = line, file = column
    def __init__(self, fen_str):
        fen = Fen_String(fen_str)
        self.board = fen.board
        self.info = fen.info
        self.king_pos = fen.king_pos

        self.legal_moves = self.get_attacking_moves()
        self.legal_moves = self.get_legal_moves()

    def __repr__(self):
        string = str()
        for rank in self.board:
            string += str(rank) + "\n"
        return string
    
    def get_info(self):
        info_copy = {key: value for key, value in self.info.items()}
        return info_copy

    def get_king_position(self):
        return self.king_pos

    def board_copy(self):
        fen = Fen_String.encryptFen(self)
        new_board = Board(fen)
        return new_board

    def move(self, move):
        def _move(copy_board, original, new):
            o_rank, o_file = original
            t_rank, t_file = new
            piece = copy_board[o_rank][o_file]
            copy_board[t_rank][t_file] = copy_board[o_rank][o_file]
            copy_board[o_rank][o_file] = No_Piece()
            if type(piece) == Pawn and Square.index_to_tile((o_rank, t_file)) == self.info["en_passant"]:
                copy_board[o_rank][t_file] = No_Piece()
            elif type(piece) == King:
                direction = -1 if t_file - o_file > 0 else 1
                o_rook_pos = len(copy_board[t_rank])-1 if t_file - o_file > 0 else 0
                rook_pos = o_rook_pos
                if abs(t_file - o_file) == 2:
                    rook = copy_board[t_rank][o_rook_pos]
                    assert type(rook) == Rook
                    while type(copy_board[t_rank][rook_pos]) != King:
                        rook_pos += direction
                    copy_board[t_rank][rook_pos+direction] = copy_board[t_rank][o_rook_pos]
                    copy_board[t_rank][o_rook_pos] = No_Piece()
            return copy_board
        original = Square.tile_to_index(move[:2])
        new = Square.tile_to_index(move[2:])
        o_rank, o_file = original
        t_rank, t_file = new
        piece = self.board[o_rank][o_file]
        capture = self.board[t_rank][t_file]
        self.board = _move(self.board_copy().board, original, new)

        #Changing board information
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
            
        if type(capture) != No_Piece or type(piece) == Pawn:
            self.info["halfmove"] = 0
        else:
            self.info["halfmove"] += 1

        if piece.colour == BLACK:
            self.info["fullmove"] += 1
        
        self.legal_moves = self.get_attacking_moves()
        self.legal_moves = self.get_legal_moves()

    def get_attacking_moves(self):
        white, black = [], []
        for rank in range(len(self.board)):
            for file in range(len(self.board[rank])):
                piece = self.board[rank][file]
                if type(piece) != No_Piece:
                    position = (rank, file)
                    possible_moves = piece.generate_moves(self, position)
                    for move in possible_moves:
                        if piece.colour:
                            white.append(Square.index_to_tile(position) + Square.index_to_tile(move))
                        else:
                            black.append(Square.index_to_tile(position) + Square.index_to_tile(move))
        #white, black = self.castling(white, black)
        self.legal_moves = {WHITE: white, BLACK: black}
        self.check_inCheck(white, black)
        self.legal_moves = {WHITE: white, BLACK: black}
        return white, black

    def get_legal_moves(self):
        w_na, b_na = [], []
        for rank in range(len(self.board)):
            for file in range(len(self.board[rank])):
                piece = self.board[rank][file]
                if type(piece) == Pawn:
                    position = (rank, file)
                    possible_moves = piece.non_attacking_moves(self, position)
                    for move in possible_moves:
                        if piece.colour:
                            w_na.append(Square.index_to_tile(position) + Square.index_to_tile(move))
                        else:
                            b_na.append(Square.index_to_tile(position) + Square.index_to_tile(move))
        #white, black = self.castling(white, black)
        self.check_inCheck(w_na, b_na)
        self.legal_moves[WHITE] += w_na
        self.legal_moves[BLACK] += b_na
        return w_na, b_na

    def castling(self, white, black):
        board = self.board
        castle_info = self.info["castling"]
        for colour in (WHITE, BLACK):
            full = "KQ" if colour else "kq"
            king_x, king_y = self.get_king_position()[colour]
            for move in set(full).intersection(set(castle_info)):
                direction = 1 if move.lower() == "k" else -1
                rook_y = king_y + direction
                piece = board[king_x][rook_y]
                success = True
                while type(piece) != Rook:
                    if type(piece) == No_Piece:
                        rook_y += direction
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
    
    def check_inCheck(self, white, black):
        king = self.get_king_position()
        for colour in king:
            legal_moves = white if colour else black
            opponent_moves = black if colour else white
            king_pos = king[colour]

            for move in range(len(legal_moves)-1, -1, -1):
                temp_board = self.board_copy()
                destination = Square.tile_to_index(legal_moves[move][2:])
                opp_moves = opponent_moves.copy()
                if type(temp_board.board[destination[0]][destination[1]]) != No_Piece:
                    for loop in range(len(opp_moves)-1, -1, -1):
                        if legal_moves[move][2:] == opp_moves[loop][2:]:
                            opp_moves.remove(opp_moves[loop])
                temp_board.move(legal_moves[move])
                if temp_board.isChecked(king_pos, opp_moves):
                    legal_moves.remove(legal_moves[move])

    def isChecked(self, king, opp_moves):
        #king = self.get_king_position()[colour]
        king = Square.index_to_tile(king)
        attacked = list()
        for move in opp_moves:
            if move[2:] == king:
                return True
        return False

    def evaluate_board(self):
        eval_w, eval_b = 0, 0
        for rank in range(len(self.board)):
            for file in range(len(self.board)):
                piece = self.board[rank][file]
                if type(piece) != No_Piece:
                    if piece.colour:
                        eval_w += piece.value + piece.piece_square[rank][file]
                    else:
                        eval_b += piece.value + piece.piece_square[rank][file]
        return eval_w, eval_b


if __name__ == "__main__":
    ex = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    a = Board(fen_str=ex)
    print(a)
    print(a.info)
    b = a.get_legal_moves()
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
    print("End passant test")

    ex = "r4rk1/pppq1p1p/2n1pnp1/3p1b2/3P4/2NBPN2/PPPQ1PPP/R3K2R w KQ - 0 1"
    a = Board(fen_str=ex)
    assert Fen_String.encryptFen(a) == ex
    print(a)
    print(a.info)
    b = a.get_legal_moves()

    a.move("a2a4")
    print(a)
    b = a.get_legal_moves()
