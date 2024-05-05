#! /bin/python3

from string import ascii_lowercase

class Square():
    """Square class"""
    def __init__(self):
        pass

    @staticmethod
    def tile_to_index(tile):
        """Converts a tile (ex: a1) to the board index(ex: (7, 0))."""
        file = ascii_lowercase.index(tile[0])
        rank = abs(int(tile[1])-8)
        return (rank, file)

    @staticmethod
    def index_to_tile(index):
        """Converts a board index to a tile."""
        rank = str(abs(index[0]-8))
        file = ascii_lowercase[index[1]]
        return file + rank

if __name__ == "__main__":
    """Testing code for conversion from tile to index and vice versa."""
    conversion = dict(zip("abcdefgh", [0, 1, 2, 3, 4, 5, 6, 7]))
    invert = {values: keys for keys, values in conversion.items()}
    for i in "abcdefgh":
        for j in [0, 1, 2, 3, 4, 5, 6, 7]:
            index = Square.tile_to_index(i+str(j))
            assert i + str(j) == Square.index_to_tile(index)
    print("All tests passed.")
