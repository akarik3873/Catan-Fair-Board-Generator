import random

class Side:
    def __init__(self, tile = None):
        self.tile = tile
        self.adj_side = []

class Tile: 
    def __init__(self, tilenum = None):
        self.sides = []
        for i in range (6):
            smth = Side()
            self.sides.append(smth)
        self.number = 0
        self.type = ""
        self.tilenum = tilenum

    def __str__ (self):
        return str(self.tilenum) + " " + str(self.number) + " " + self.type