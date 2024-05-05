#! /bin/python3

from pieces import *
from fen import *
from squares import *

class Board():
    """
    Board class
    Takes a FEN string as input (which is a string representation of the board)
    """
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
        """Returns board information"""
        info_copy = {key: value for key, value in self.info.items()}
        return info_copy

    def get_king_position(self):
        """Returns the position of both kings"""
        return self.king_pos

    def board_copy(self):
        """Returns a copy of the board object"""
        fen = Fen_String.encryptFen(self)
        new_board = Board(fen)
        return new_board

    def move(self, move):
        """
        Move function
        move (str): String of the form "a1b1", for example, where a1 is the original tile and b1 is the new tile. The tile names follow typical chess notation, where a1 is the bottom left of the board, and h8 is the top right.
        This function also modifies all the other information of the board, in accordance with the chosen move.
        """
        def _move(board, o_rank, o_file, t_rank, t_file):
            """
            Helper function for move()
            board: A board object
            o_rank, o_file, t_rank, t_file (int): Coordinates of the original tile, and new tile respectively.
            """
            copy_board = board.board
            piece = copy_board[o_rank][o_file]
            copy_board[t_rank][t_file] = copy_board[o_rank][o_file]     #puts the piece at the new square
            copy_board[o_rank][o_file] = No_Piece()         #Replaces the original tile of the piece with No_Piece
            board.board = copy_board
            if type(piece) == Pawn:
                if Square.index_to_tile((o_rank, t_file)) == self.info["en_passant"]:       #Taking a pawn with the "en passant" rule
                    copy_board[o_rank][t_file] = No_Piece()
                elif t_rank == 0 or t_rank == 7:        #Rule for promotion. It defaults to promoting a pawn to a queen.
                    copy_board[t_rank][t_file] = Queen(piece.colour)
            elif type(piece) == King:       #Move for castling
                if t_file - o_file == 2 and piece.colour:
                    copy_board = _move(board.board_copy(), 7, 7, 7, 5)      #Function calls itself again to move the rook (king was already moved)
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

        #For when the user tries to castle
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
        """
        Gets all the moves that can check the opposing king (attacking moves).
        colour (int/bool): Colour of the pieces for which we are checking the attacking moves for. 
        """
        moves = list()
        for rank in range(len(self.board)):
            for file in range(len(self.board[rank])):
                piece = self.board[rank][file]
                if type(piece) != No_Piece and piece.colour == colour:
                    position = (rank, file)
                    possible_moves = piece.generate_moves(self, position)
                    for move in possible_moves:
                        moves.append(Square.index_to_tile(position) + Square.index_to_tile(move))           #Appends attacking move to moves list and converting position tuples into a string.
        moves = self.castling(moves.copy(), colour)     #Adds castling moves to list
        self.attacking_moves = moves
        return moves

    def get_legal_moves(self, colour):
        """
        Gets all the legal moves (including pawn pushes).
        colour (int/bool): Colour of the pieces for which we are checking the legal moves for. 
        """
        moves = list()
        for rank in range(len(self.board)):
            for file in range(len(self.board[rank])):
                piece = self.board[rank][file]
                if type(piece) != No_Piece and piece.colour == colour:
                    position = (rank, file)
                    if type(piece) == Pawn:
                        possible_moves = piece.non_attacking_moves(self, position)
                        for move in possible_moves:
                            moves.append(Square.index_to_tile(position) + Square.index_to_tile(move))       #Appends each pawn push to the moves list and converting position tuples into a string.
                    possible_moves = piece.generate_moves(self, position)
                    for move in possible_moves:
                        moves.append(Square.index_to_tile(position) + Square.index_to_tile(move))           #Appends attacking move to moves list and converting position tuples into a string.
        moves = self.castling(moves.copy(), colour)     #Adds castling moves to list
        moves = self.validMoves(moves.copy(), colour)       #Checks if each move is a valid move
        self.legal_moves = moves
        return moves

    def castling(self, moves, colour):
        """
        Gets the possible castling moves for a colour of pieces.
        moves (list): List of calculated moves.
        colour (int/bool): Colour of the pieces for which we are checking the castling moves for. 
        """
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
            if r_move in moves and k_move in moves:         #If the rook is able to move to a certain square and the king can move over one square, castling may be possible (since there are no pieces blocking the path).
                moves.append(Square.index_to_tile((king_x, king_y)) + Square.index_to_tile((king_x, king_y + k_dir)))
        return moves
    
    def validMoves(self, moves, colour):
        """
        Checks if the moves in the list are valid, meaning that after a piece is moved, its king is not checked (checks if a piece is pinned).
        moves (list): List of calculated moves.
        colour (int/bool): Colour of the pieces for which we are checking the moves for. 
        """
        for move in range(len(moves)-1, -1, -1):        #Iterates backwards, so that if a move is removed, it does not affect the loop.
            temp_board = self.board_copy()
            temp_board.move(moves[move])            #Uses a naive approach, by copying the board, and performing each move to see if the king is checked.
            king_pos = temp_board.get_king_position()[colour]

            opp_moves = temp_board.get_attacking_moves(0 if colour else 1)
            if temp_board.isChecked(king_pos, opp_moves):
                moves.remove(moves[move])           #If the king is checked after making a certain move, that move is not valid.
        return moves
            

    def isChecked(self, king, opp_moves):
        """
        Checks if a king is checked by checking if the king's tile is attacked.
        king (tuple): Position of the king
        opp_moves (list): Attacking moves of the opponent of the king.
        """
        king = Square.index_to_tile(king)
        for move in opp_moves:
            if move[2:] == king:
                return True
        return False

    def evaluate_board(self, max_player):
        """
        Evaluates the board position for the maximizing player
        max_player (int/bool): Maximizing player. 
        """
        eval_w, eval_b = 0, 0
        for rank in range(len(self.board)):
            for file in range(len(self.board)):
                piece = self.board[rank][file]
                if type(piece) != No_Piece:
                    if piece.colour:
                        eval_w += piece.value + piece.piece_square[rank][file]      #The evaluation for a specific piece, is its value + the value of its position on the board.
                    else:
                        eval_b += piece.value + piece.piece_square[rank][file]
        eval = eval_w - eval_b if max_player else eval_b - eval_w       #Calculates the evaluation of the board for a specific player.
        return eval

    def game_over(self, repetition=[]):
        """
        Checks if the game is over.
        repetition (list): List of moves that are equal to the last move that was done. If the length is 3 or higher, there is a repetition of moves.
        """
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
    """Initial tests for the Board class. These tests may no longer be valid anymore since the class was modified a lot since then."""
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
