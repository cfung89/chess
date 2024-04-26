#! /bin/python3

from squares import *

BLACK = 0
WHITE = 1

class Vector(tuple):
    def __add__(self, other):
        '''Add two vectors.'''
        r = []
        for a, b in zip(self, other):
            r.append(a + b)
        return Vector(r)

class Piece(object):
    def __init__(self, colour):
        self.colour = colour

    def __repr__(self):
        return f"{self.name}"

    @staticmethod
    def translate(name):
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
        """Generates moves for Rook, Bishop, and Queen"""
        board = board_obj.board
        moves = list()
        directions = self.directions
        for direction in directions:
            changing = Vector((position[0], position[1]))
            changing += direction
            while 0 <= changing[0] <= 7 and 0 <= changing[1] <= 7:
                rank, file = changing[0], changing[1]
                if type(board[rank][file]) == No_Piece:
                    moves.append((rank, file))
                    changing += direction
                    continue
                elif board[rank][file].colour != self.colour:
                    moves.append((rank, file))
                    piece = board[rank + direction[0]][file + direction[1]]
                break
        return moves


class Pawn(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.name = "P" if colour else "p"
        self.value = 100

    def generate_moves(self, board_obj, position):
        moves = list()
        na_moves = list()
        board = board_obj.board
        en_passant = board_obj.info["en_passant"]
        rank, file = position[0], position[1]
        if self.colour:
            #Check for push
            for forward in range(2 if position[0]==6 else 1):
                rank -= 1
                if rank >= 0 and type(board[rank][file]) == No_Piece:
                    na_moves.append((rank, file))
                else:
                    break

            #Check for capture
            rank = position[0]-1
            if rank >= 0 and file-1 >= 0 and type(board[rank][file-1]) != No_Piece and board[rank][file-1].colour != self.colour:
                moves.append((rank, file-1))
            if rank >= 0 and file+1 <= 7 and type(board[rank][file+1]) != No_Piece and board[rank][file+1].colour != self.colour:
                moves.append((rank, file+1))

            #Check for en passant
            if en_passant != "-":
                pawn = Square.tile_to_index(en_passant)
                if position[0] == pawn[0]:
                    if position[1] == pawn[1]-1:
                        moves.append((position[0]-1, position[1]+1))
                    elif position[1] == pawn[1]+1:
                        moves.append((position[0]-1, position[1]-1))
        else:
            #Check for push
            for forward in range(2 if position[0]==1 else 1):
                rank += 1
                if rank <= 7 and type(board[rank][file]) == No_Piece:
                    na_moves.append((rank, file))
                else:
                    break

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
        return moves, na_moves


class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.name = "R" if colour else "r"
        self.directions = [Vector((-1, 0)), Vector((1, 0)), Vector((0, -1)), Vector((0, 1))]
        self.value = 500

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

        """
        self.directions = list()
        for i in (-1, 1, -2, 2):
            for j in (-1, 1, -2, 2):
                if abs(i) != abs(j):
                    self.directions.append(Vector((i, j)))
        """

    def generate_moves(self, board_obj, position):
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
        a, b = Rook(WHITE), Bishop(WHITE)
        self.directions = a.directions + b.directions
        self.value = 900

class King(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.name = "K" if colour else "k"
        self.directions = [Vector((-1, -1)), Vector((-1, 0)), Vector((-1, 1)), Vector((0, -1)), Vector((0, 1)), Vector((1, -1)), Vector((1, 0)), Vector((1, 1))]
        self.value = 20000

        """
        self.directions = list()
        for i in (-1, 1, 0):
            for j in (-1, 1, 0):
                self.directions.append(Vector((i, j)))
        self.directions.remove(Vector((0, 0))
        """

    def generate_moves(self, board_obj, position):
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
    def __init__(self):
        self.name = "."

    def __repr__(self):
        return self.name

if __name__ == "__main__":
    a = Pawn(WHITE)
    print(a.name)
    b = Knight(WHITE)
    print(b.directions)
