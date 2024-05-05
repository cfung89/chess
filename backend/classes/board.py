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
        def _move(board, o_rank, o_file, t_rank, t_file):
            copy_board = board.board
            piece = copy_board[o_rank][o_file]
            copy_board[t_rank][t_file] = copy_board[o_rank][o_file]
            copy_board[o_rank][o_file] = No_Piece()
            board.board = copy_board
            if type(piece) == Pawn:
                if Square.index_to_tile((o_rank, t_file)) == self.info["en_passant"]:
                    copy_board[o_rank][t_file] = No_Piece()
                elif t_rank == 0 or t_rank == 7:
                    copy_board[t_rank][t_file] = Queen(piece.colour)
            elif type(piece) == King:
                if t_file - o_file == 2 and piece.colour:
                    copy_board = _move(board.board_copy(), 7, 7, 7, 5)
                elif t_file - o_file == -2 and piece.colour:
                    copy_board = _move(board.board_copy(), 7, 0, 7, 3)
                elif t_file - o_file == 2 and not piece.colour:
                    copy_board = _move(board.board_copy(), 0, 7, 0, 5)
                elif t_file - o_file == -2 and not piece.colour:
                    copy_board = _move(board.board_copy(), 0, 0, 0, 3)
            return copy_board
        o_rank, o_file = Square.tile_to_index(move[:2])
        t_rank, t_file = Square.tile_to_index(move[2:])
        piece = self.board[o_rank][o_file]
        capture = self.board[t_rank][t_file]
        if type(piece) == King:
            if t_file - o_file == 3:
                t_file = 6
            elif t_file - o_file == -4:
                t_file = 2
        self.board = _move(self.board_copy(), o_rank, o_file, t_rank, t_file)

        #Changing board information
        self.info["side"] = BLACK if self.info["side"] else WHITE

        if type(piece) == Pawn:
            if abs(t_rank - o_rank) == 2:
                self.info["en_passant"] = move[2:]
            else:
                self.info["en_passant"] = "-"
        elif type(piece) == King:
            if self.info["castling"] != "-":
                if str(piece).isupper():
                    self.info["castling"].replace("KQ", "")
                else:
                    self.info["castling"].replace("kq", "")
                if not self.info["castling"]:
                    self.info["castling"] = "-"
            self.king_pos[piece.colour] = (t_rank, t_file)
        elif type(piece) == Rook:
            if self.info["castling"] != "-":
                if o_rank == 7 and o_file == 7:
                    self.info["castling"].replace("K", "")
                elif o_rank == 7 and o_file == 0:
                    self.info["castling"].replace("Q", "")
                elif o_rank == 0 and o_file == 7:
                    self.info["castling"].replace("k", "")
                elif o_rank == 0 and o_file == 0:
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
        moves = list()
        for rank in range(len(self.board)):
            for file in range(len(self.board[rank])):
                piece = self.board[rank][file]
                if type(piece) != No_Piece and piece.colour == colour:
                    position = (rank, file)
                    possible_moves = piece.generate_moves(self, position)
                    for move in possible_moves:
                        moves.append(Square.index_to_tile(position) + Square.index_to_tile(move))
        moves = self.castling(moves.copy(), colour)
        self.attacking_moves = moves
        return moves

    def get_legal_moves(self, colour):
        moves = list()
        for rank in range(len(self.board)):
            for file in range(len(self.board[rank])):
                piece = self.board[rank][file]
                if type(piece) != No_Piece and piece.colour == colour:
                    position = (rank, file)
                    if type(piece) == Pawn:
                        possible_moves = piece.non_attacking_moves(self, position)
                        for move in possible_moves:
                            moves.append(Square.index_to_tile(position) + Square.index_to_tile(move))
                    possible_moves = piece.generate_moves(self, position)
                    for move in possible_moves:
                        moves.append(Square.index_to_tile(position) + Square.index_to_tile(move))
        moves = self.castling(moves.copy(), colour)
        moves = self.validMoves(moves.copy(), colour)
        self.legal_moves = moves
        return moves

    def castling(self, moves, colour):
        castle_info = self.info["castling"]
        full = "KQ" if colour else "kq"
        king_x, king_y = self.king_pos[colour]
        for move in set(full).intersection(set(castle_info)):
            r_dir, rook_x, k_dir = 0, 0, 0
            if move.lower() == "k":
                rook_x = 7
                r_dir = -2
                k_dir = 2
            else:
                rook_x = 0
                r_dir = 3
                k_dir = -2
            r_move = Square.index_to_tile((king_x, rook_x)) + Square.index_to_tile((king_x, rook_x + r_dir))
            k_move = Square.index_to_tile((king_x, king_y)) + Square.index_to_tile((king_x, king_y + k_dir//2))
            if r_move in moves and k_move in moves:
                moves.append(Square.index_to_tile((king_x, king_y)) + Square.index_to_tile((king_x, king_y + k_dir)))
        return moves
    
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
        return eval

    def game_over(self, repetition=[]):
        if len(repetition) >= 3:
            return 4        #draw by repetition
        
        turn = self.info["side"]
        king = self.king_pos[turn]

        if self.isChecked(king, self.get_attacking_moves(0 if turn else 1)):
            if not self.legal_moves:       #change the condition
                return 1        #checkmate
            else:
                return 0
        elif not self.legal_moves:
            return 2        #stalemate

        if self.info["halfmove"] >= 100:        #and side to move has at least one legal move
            return 3    #50-move draw
        return 0

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
