#! /bin/python3

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
        def _move(board, original, new):
            copy_board = board.board
            o_rank, o_file = original
            t_rank, t_file = new
            piece = copy_board[o_rank][o_file]
            """
            print(piece.colour, board.get_info())
            assert board.get_info()["side"] == piece.colour
            """
            copy_board[t_rank][t_file] = copy_board[o_rank][o_file]
            copy_board[o_rank][o_file] = No_Piece()
            if type(piece) == Pawn:
                if Square.index_to_tile((o_rank, t_file)) == self.info["en_passant"]:
                    copy_board[o_rank][t_file] = No_Piece()
                elif t_rank == 0 or t_rank == 7:
                    copy_board[t_rank][t_file] = Queen(piece.colour)
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
        self.board = _move(self.board_copy(), original, new)

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

    def get_attacking_moves(self, colour):
        moves = []
        for rank in range(len(self.board)):
            for file in range(len(self.board[rank])):
                piece = self.board[rank][file]
                if type(piece) != No_Piece and piece.colour == colour:
                    position = (rank, file)
                    possible_moves = piece.generate_moves(self, position)
                    for move in possible_moves:
                        moves.append(Square.index_to_tile(position) + Square.index_to_tile(move))
        return moves

    def get_legal_moves(self, colour):
        moves = self.get_attacking_moves(colour)
        for rank in range(len(self.board)):
            for file in range(len(self.board[rank])):
                piece = self.board[rank][file]
                if type(piece) == Pawn and piece.colour == colour:
                    position = (rank, file)
                    possible_moves = piece.non_attacking_moves(self, position)
                    for move in possible_moves:
                        moves.append(Square.index_to_tile(position) + Square.index_to_tile(move))
        moves = self.validMoves(moves.copy(), colour)
        return moves

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
    
    def validMoves(self, moves, colour):
        for move in range(len(moves)-1, -1, -1):
            temp_board = self.board_copy()
            temp_board.move(moves[move])
            king_pos = temp_board.get_king_position()[colour]

            opp_moves = temp_board.get_attacking_moves(0 if colour else 1)
            if temp_board.isChecked(king_pos, opp_moves):
                moves.remove(moves[move])
        return moves
            

    def isChecked(self, king, opp_moves):
        king = Square.index_to_tile(king)
        for move in opp_moves:
            if move[2:] == king:
                return True
        return False

    def evaluate_board(self, max_player):
        eval_w, eval_b = 0, 0
        for rank in range(len(self.board)):
            for file in range(len(self.board)):
                piece = self.board[rank][file]
                if type(piece) != No_Piece:
                    if piece.colour:
                        eval_w += piece.value + piece.piece_square[rank][file]
                    else:
                        eval_b += piece.value + piece.piece_square[rank][file]
        eval = eval_w - eval_b if max_player else eval_b - eval_w
        #print(max_player, eval_w, eval_b, eval)
        return eval


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
