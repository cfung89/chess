#! /bin/python3

from board import *
from pieces import *

class Game():
    def __init__(self, fen, user_colour):
        self.human = user_colour
        self.computer = Game.get_opponent(self.human)
        self.positions = list()
