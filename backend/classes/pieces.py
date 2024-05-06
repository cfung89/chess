#! /bin/python3

from squares import *

BLACK = 0
WHITE = 1

class Vector(tuple):
    """Vector class"""
    def __add__(self, other):
        '''Add two vectors to generate piece moves.'''
        r = []
        for a, b in zip(self, other):
            r.append(a + b)
        return Vector(r)

class Piece(object):
    """Piece object"""
    def __init__(self, colour):
        """
        Almost every piece has 5 attributes:
        - Colour (int): 0 if it is a black piece, and 1 if it is a white piece.
        - Name (str): String of length 1, where if the letter is capitalized, it is a white piece, or else, it is a black piece.
        - Value (int): Value of a (type of) piece.
        - Piece_square (list): Matrix board representation where each entry is the evaluation of the piece at that specific position. This is because a piece's position is important in the overall board evaluation. This matrix depends on the colour of the piece.
        - Directions (list): List of 2D unit vectors that point towards the directions a piece can move in.
        """
        self.colour = colour

    def __repr__(self):
        return f"{self.name}"

    @staticmethod
    def translate(name):
        """Translates the name of a piece to a specific piece object (with a specific colour). This is used in the Fen_String object, to convert from string to Board representation."""
        colour = None
        if name.islower():
            colour = BLACK
        else:
            colour = WHITE

        name = name.lower()
        if name == "p":
            return Pawn(colour)
        elif name == "r":
            return Rook(colour)
        elif name == "n":
            return Knight(colour)
        elif name == "b":
            return Bishop(colour)
        elif name == "q":
            return Queen(colour)
        else:
            return King(colour)


    def generate_moves(self, board_obj, position):
        """
        Generates moves for Rook, Bishop, and Queen. Knights, Kings and Pawns do not continue moving in a direction indefinitely.
        board_obj: Board object
        position (tuple): Position of the piece to generate moves from. This tuple is of the form (rank, file).
        """
        board = board_obj.board
        moves = list()
        directions = self.directions
        for direction in directions:        #For each direction
            changing = Vector((position[0], position[1]))
            changing += direction   #Adds the direction to the current position (ie. the piece moves once in the direction of the unit vector)
            while 0 <= changing[0] <= 7 and 0 <= changing[1] <= 7:
                rank, file = changing[0], changing[1]
                if type(board[rank][file]) == No_Piece:     #if there is no piece, then this is a valid move
                    moves.append((rank, file))
                    changing += direction
                    continue
                elif board[rank][file].colour != self.colour:       #If there is a piece, and it is of the opposite colour, this piece can be captured, but the moving piece cannot go further in this direction
                    moves.append((rank, file))
                break
        return moves


class Pawn(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.name = "P" if colour else "p"
        self.value = 100
        if self.colour:
            self.piece_square = [[0, 0, 0, 0, 0, 0, 0, 0], [50, 50, 50, 50, 50, 50, 50, 50], [10, 10, 20, 30, 30, 20, 10, 10], [5, 5, 10, 25, 25, 10, 5, 5], [0, 0, 0, 20, 20, 0, 0, 0], [5, -5, -10, 0, 0, -10, -5, 5], [5, 10, 10, -20, -20, 10, 10, 5], [0, 0, 0, 0, 0, 0, 0, 0]]
        else:
            self.piece_square = [[0, 0, 0, 0, 0, 0, 0, 0], [5, 10, 10, -20, -20, 10, 10, 5], [5, -5, -10, 0, 0, -10, -5, 5], [0, 0, 0, 20, 20, 0, 0, 0], [5, 5, 10, 25, 25, 10, 5, 5], [10, 10, 20, 30, 30, 20, 10, 10], [50, 50, 50, 50, 50, 50, 50, 50], [0, 0, 0, 0, 0, 0, 0, 0]]

    def non_attacking_moves(self, board_obj, position):
        """
        Generates pawn push moves.
        board_obj: Board object
        position (tuple): Position of the piece to generate moves from. This tuple is of the form (rank, file).
        """
        na_moves = list()
        board = board_obj.board
        rank, file = position[0], position[1]
        if self.colour:
            for forward in range(2 if position[0]==6 else 1):       #Pawns can only be pushed 2 squares forward if they are on their starting squares
                rank -= 1
                if rank >= 0 and type(board[rank][file]) == No_Piece:
                    na_moves.append((rank, file))
                else:
                    break
        else:
            for forward in range(2 if position[0]==1 else 1):
                rank += 1
                if rank <= 7 and type(board[rank][file]) == No_Piece:
                    na_moves.append((rank, file))
                else:
                    break
        return na_moves

    def generate_moves(self, board_obj, position):
        """
        Generates pawn moves (capturing and en passant).
        board_obj: Board object
        position (tuple): Position of the piece to generate moves from. This tuple is of the form (rank, file).
        """
        moves = list()
        board = board_obj.board
        en_passant = board_obj.info["en_passant"]
        rank, file = position[0], position[1]
        if self.colour:
            #Check for capture
            rank = position[0]-1
            if rank >= 0 and file-1 >= 0 and type(board[rank][file-1]) != No_Piece and board[rank][file-1].colour != self.colour:
                moves.append((rank, file-1))
            if rank >= 0 and file+1 <= 7 and type(board[rank][file+1]) != No_Piece and board[rank][file+1].colour != self.colour:
                moves.append((rank, file+1))

            #Check for en passant
            if en_passant != "-":
                pawn = Square.tile_to_index(en_passant)
                if position[0] == pawn[0]:      #Conditional statements to check if the pawn is at the correct position to do en passant.
                    if position[1] == pawn[1]-1:
                        moves.append((position[0]-1, position[1]+1))
                    elif position[1] == pawn[1]+1:
                        moves.append((position[0]-1, position[1]-1))
        else:

            #Check for capture
            rank = position[0]+1
            if rank <= 7 and file-1 >= 0 and type(board[rank][file-1]) != No_Piece and board[rank][file-1].colour != self.colour:
                moves.append((rank, file-1))
            if rank <= 7 and file+1 <= 7 and type(board[rank][file+1]) != No_Piece and board[rank][file+1].colour != self.colour:
                moves.append((rank, file+1))

            #Check for en passant
            if en_passant != "-":
                pawn = Square.tile_to_index(en_passant)
                if position[0] == pawn[0]:
                    if position[1] == pawn[1]-1:
                        moves.append((position[0]+1, position[1]+1))
                    elif position[1] == pawn[1]+1:
                        moves.append((position[0]+1, position[1]-1))
        return moves


class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.name = "R" if colour else "r"
        self.directions = [Vector((-1, 0)), Vector((1, 0)), Vector((0, -1)), Vector((0, 1))]
        self.value = 500
        if self.colour:
            self.piece_square = [[0, 0, 0, 0, 0, 0, 0, 0], [5, 10, 10, 10, 10, 10, 10, 5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [0, 0, 0, 5, 5, 0, 0, 0]]
        else:
            self.piece_square = [[0, 0, 0, 5, 5, 0, 0, 0], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [5, 10, 10, 10, 10, 10, 10, 5], [0, 0, 0, 0, 0, 0, 0, 0]]

        #The code (and all following similar code) was used to generate the directions list.
        """
        self.directions = list()
        for i in (-1, 0, 1):
            for j in (-1, 0,  1):
                if abs(i) != abs(j):
                    self.directions.append(Vector((i, j)))
        """

class Knight(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.name = "N" if colour else "n"
        self.directions = [Vector((-1, -2)), Vector((-1, 2)), Vector((1, -2)), Vector((1, 2)), Vector((-2, -1)), Vector((-2, 1)), Vector((2, -1)), Vector((2, 1))]
        self.value = 320
        if self.colour:
            self.piece_square = [[-50, -40, -30, -30, -30, -30, -40, -50], [-40, -20, 0, 0, 0, 0, -20, -40], [-30, 0, 10, 15, 15, 10, 0, -30], [-30, 5, 15, 20, 20, 15, 5, -30], [-30, 0, 15, 20, 20, 15, 0, -30], [-30, 5, 10, 15, 15, 10, 5, -30], [-40, -20, 0, 5, 5, 0, -20, -40], [-50, -40, -30, -30, -30, -30, -40, -50]]
        else:
            self.piece_square = [[-50, -40, -30, -30, -30, -30, -40, -50], [-40, -20, 0, 5, 5, 0, -20, -40], [-30, 5, 10, 15, 15, 10, 5, -30], [-30, 0, 15, 20, 20, 15, 0, -30], [-30, 5, 15, 20, 20, 15, 5, -30], [-30, 0, 10, 15, 15, 10, 0, -30], [-40, -20, 0, 0, 0, 0, -20, -40], [-50, -40, -30, -30, -30, -30, -40, -50]]

        """
        self.directions = list()
        for i in (-1, 1, -2, 2):
            for j in (-1, 1, -2, 2):
                if abs(i) != abs(j):
                    self.directions.append(Vector((i, j)))
        """

    def generate_moves(self, board_obj, position):
        """
        Generates knight moves.
        board_obj: Board object
        position (tuple): Position of the piece to generate moves from. This tuple is of the form (rank, file).
        """
        board = board_obj.board
        moves = list()
        directions = self.directions
        for direction in directions:
            changing = Vector((position[0], position[1]))
            changing += direction
            if 0 <= changing[0] <= 7 and 0 <= changing[1] <= 7:
                rank, file = changing[0], changing[1]
                if type(board[rank][file]) == No_Piece:
                    moves.append((rank, file))
                    changing += direction
                    continue
                elif board[rank][file].colour != self.colour:
                    moves.append((rank, file))
        return moves

class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.name = "B" if colour else "b"
        self.directions = [Vector((-1, -1)), Vector((-1, 1)), Vector((1, -1)), Vector((1, 1))]
        self.value = 330
        if self.colour:
            self.piece_square = [[-20, -10, -10, -10, -10, -10, -10, -20], [-10, 0, 0, 0, 0, 0, 0, -10], [-10, 0, 5, 10, 10, 5, 0, -10], [-10, 5, 5, 10, 10, 5, 5, -10], [-10, 0, 10, 10, 10, 10, 0, -10], [-10, 10, 10, 10, 10, 10, 10, -10], [-10, 5, 0, 0, 0, 0, 5, -10], [-20, -10, -10, -10, -10, -10, -10, -20]]
        else:
            self.piece_square = [[-20, -10, -10, -10, -10, -10, -10, -20], [-10, 5, 0, 0, 0, 0, 5, -10], [-10, 10, 10, 10, 10, 10, 10, -10], [-10, 0, 10, 10, 10, 10, 0, -10], [-10, 5, 5, 10, 10, 5, 5, -10], [-10, 0, 5, 10, 10, 5, 0, -10], [-10, 0, 0, 0, 0, 0, 0, -10], [-20, -10, -10, -10, -10, -10, -10, -20]]

        """
        self.directions = list()
        for i in (-1, 1):
            for j in (-1, 1):
                self.directions.append(Vector((i, j)))
        """
        
class Queen(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.name = "Q" if colour else "q"
        self.directions = [Vector((-1, -1)), Vector((-1, 1)), Vector((1, -1)), Vector((1, 1))] + [Vector((-1, 0)), Vector((1, 0)), Vector((0, -1)), Vector((0, 1))]     #Directions list is just the directions of the bishop + the rook
        self.value = 900
        if self.colour:
            self.piece_square = [[-20, -10, -10, -5, -5, -10, -10, -20], [-10, 0, 0, 0, 0, 0, 0, -10], [-10, 0, 5, 5, 5, 5, 0, -10], [-5, 0, 5, 5, 5, 5, 0, -5], [0, 0, 5, 5, 5, 5, 0, -5], [-10, 5, 5, 5, 5, 5, 0, -10], [-10, 0, 5, 0, 0, 0, 0, -10], [-20, -10, -10, -5, -5, -10, -10, -20]]
        else:
            self.piece_square = [[-20, -10, -10, -5, -5, -10, -10, -20], [-10, 0, 0, 0, 0, 5, 0, -10], [-10, 0, 5, 5, 5, 5, 5, -10], [-5, 0, 5, 5, 5, 5, 0, 0], [-5, 0, 5, 5, 5, 5, 0, -5], [-10, 0, 5, 5, 5, 5, 0, -10], [-10, 0, 0, 0, 0, 0, 0, -10], [-20, -10, -10, -5, -5, -10, -10, -20]]

class King(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.name = "K" if colour else "k"
        self.directions = [Vector((-1, -1)), Vector((-1, 0)), Vector((-1, 1)), Vector((0, -1)), Vector((0, 1)), Vector((1, -1)), Vector((1, 0)), Vector((1, 1))]
        self.value = 20000
        if self.colour:
            self.piece_square = [[-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30], [-20, -30, -30, -40, -40, -30, -30, -20], [-10, -20, -20, -20, -20, -20, -20, -10], [20, 20, 0, 0, 0, 0, 20, 20], [20, 30, 10, 0, 0, 10, 30, 20]]
        else:
            self.piece_square = [[20, 30, 10, 0, 0, 10, 30, 20], [20, 20, 0, 0, 0, 0, 20, 20], [-10, -20, -20, -20, -20, -20, -20, -10], [-20, -30, -30, -40, -40, -30, -30, -20], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30]]

        """
        self.directions = list()
        for i in (-1, 1, 0):
            for j in (-1, 1, 0):
                self.directions.append(Vector((i, j)))
        self.directions.remove(Vector((0, 0))
        """

    def generate_moves(self, board_obj, position):
        """
        Generates king moves.
        board_obj: Board object
        position (tuple): Position of the piece to generate moves from. This tuple is of the form (rank, file).
        """
        board = board_obj.board
        moves = list()
        directions = self.directions
        for direction in directions:
            changing = Vector((position[0], position[1]))
            changing += direction
            if 0 <= changing[0] <= 7 and 0 <= changing[1] <= 7:
                rank, file = changing[0], changing[1]
                if type(board[rank][file]) == No_Piece:
                    moves.append((rank, file))
                    changing += direction
                    continue
                elif board[rank][file].colour != self.colour:
                    moves.append((rank, file))
        return moves

class No_Piece():
    """No_Piece class"""
    def __init__(self):
        self.name = "."

    def __repr__(self):
        return self.name

if __name__ == "__main__":
    """Testing code"""
    a = Pawn(WHITE)
    print(a.name)
    b = Knight(WHITE)
    print(b.directions)
