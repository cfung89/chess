#! /bin/python3

from string import ascii_lowercase

class Square():
    def __init__(self):
        pass

    @staticmethod
    def tile_to_index(tile):
        file = ascii_lowercase.index(tile[0])
        rank = abs(int(tile[1])-8)
        return (rank, file)

    @staticmethod
    def index_to_tile(index):
        rank = str(abs(index[0]-8))
        file = ascii_lowercase[index[1]]
        return file + rank

if __name__ == "__main__":
    conversion = dict(zip("abcdefgh", [0, 1, 2, 3, 4, 5, 6, 7]))
    invert = {values: keys for keys, values in conversion.items()}
    for i in "abcdefgh":
        for j in [0, 1, 2, 3, 4, 5, 6, 7]:
            index = Square.tile_to_index(i+str(j))
            assert i + str(j) == Square.index_to_tile(index)
    print("All tests passed.")
