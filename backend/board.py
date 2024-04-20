#! /bin/python3

from copy import deepcopy
from pieces import *
from fen import *
from squares import *

class Board():
    #Rank = line, file = column
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
        original = Square.tile_to_index(move[:2])
        new = Square.tile_to_index(move[2:])
        o_rank, o_file = original
        t_rank, t_file = new
        white, black, w_boards, b_boards = self.get_legal_moves()
        piece = self.board[o_rank][o_file]
        capture = self.board[t_rank][t_file]
        if piece.colour:
            ind = white[original].index(new)
            self.board = w_boards[original][ind]
        else:
            ind = black[original].index(new)
            self.board = b_boards[original][ind]

        o_rank, o_file = original
        t_rank, t_file = new
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

    def get_legal_moves(self):
        def _move(copy_board, original, new, king_pos):
            o_rank, o_file = original
            t_rank, t_file = new
            piece = copy_board[o_rank][o_file]
            copy_board[t_rank][t_file] = copy_board[o_rank][o_file]
            copy_board[o_rank][o_file] = No_Piece()
            if type(piece) == Pawn and Square.index_to_tile((o_rank, t_file)) == self.info["en_passant"]:
                copy_board[o_rank][t_file] = No_Piece()
            elif type(piece) == King:
                king_pos = (t_rank, t_file)
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
            return copy_board, king_pos

        white, black, w_boards, b_boards = dict(), dict(), dict(), dict()
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
            king_pos = self.get_king_position()[colour]

            for o_pos in legal_moves:
                for ind in range(len(legal_moves[o_pos])):
                    move = legal_moves[o_pos][ind]
                    temp_board, king_pos = _move(self.board_copy(), o_pos, move, king_pos)
                    temp_board = Board(board=temp_board, king_pos=king_pos)
                    temp_opp = deepcopy(opponent_moves)
                    if type(temp_board.board[move[0]][move[1]]) != No_Piece:
                        temp_opp[move] = []
                    if temp_board.isChecked(king_pos, colour, temp_opp):
                        legal_moves[o_pos][ind] = "-"
                    elif colour:
                        if o_pos not in w_boards:
                            w_boards[o_pos] = [temp_board.board]
                        else:
                            w_boards[o_pos].append(temp_board.board)
                    else:
                        if o_pos not in b_boards:
                            b_boards[o_pos] = [temp_board.board]
                        else:
                            b_boards[o_pos].append(temp_board.board)
                legal_moves[o_pos] = [i for i in legal_moves[o_pos] if i != "-"]

            """
            pos = self.get_king_position()[colour]
            king_moves = set(legal_moves.pop(pos))
            temp = set(Board.get_moves(opponent_moves))
            king_moves = list(king_moves - temp)
            legal_moves[pos] = king_moves
            """
        return white, black, w_boards, b_boards

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

    def isChecked(self, king, colour, opp_moves):
        #king = self.get_king_position()[colour]
        attacked = Board.get_moves(opp_moves)
        if king in attacked:
            return True
        return False



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
