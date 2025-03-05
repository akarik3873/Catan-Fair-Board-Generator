import random
import Node_Class
class Tile: 
    def __init__(self, tilenum = None):
        self.sides = [Side] * 6 
        self.number = 0
        self.type = ""
        self.tilenum = tilenum

class Side:
    def __init__(self, tile = None):
        self.tile = tile
        self.adj_side = []

class Board:
    def __init__(self):
        self.numbers = {}
        self.types = {}
        self.ports = [["Water", "Water", "Wood", "Wood", "Water"], 
                 ["Wheat", "Wheat", "Water", "Water", "Water"], 
                 ["Water", "Water", "Rock", "Rock", "Water"], 
                 ["Sheep", "Sheep", "Water", "Water", "Water"], 
                 ["Water", "Water", "Water", "Water", "Water"],
                 ["Brick", "Brick", "Water", "Water", "Water"]]
        self.board = []
        for i in range (19):
            smth = Tile()
            self.board.append(smth)
        self.tile_type = {"Wheat": 4, "Sheep": 4, "Wood": 4, "Brick": 3, "Stone": 3, "Desert": 1}
        self.tile_types = ["Wheat", "Sheep", "Wood", "Brick", "Stone", "Desert"] 
        self.tile_num = {2:1, 3:2, 4:2, 5:2, 6:2, 7:1, 8:2, 9:2, 10:2, 11:2, 12:1}
        self.tile_nums = list(range(2, 13))
        self.checks = [self.alwaysTrue, self.two_brone]
        for i in range(19):
            self.board[i].tilenum = i
# establishing first tile 
        for i in range(6):
            self.board[18].sides[i].tile = self.board[i]
# create a linked list head to cut down on the if statements   
# establishing the inner ring      
        for i in range(6):
            self.board[i].sides[0].tile = self.board[18]
            self.board[i].sides[1].tile = self.board[i + 1]
            self.board[i].sides[2].tile = self.board[2 * i + 5]
            self.board[i].sides[3].tile = self.board[2 * i + 6]
            self.board[i].sides[4].tile = self.board[2 * i + 7]
            self.board[i].sides[5].tile = self.board[i + 1]
            if i == 0:
                self.board[i].sides[5].tile = self.board[5]
                self.board[i].sides[2].tile  = self.board[17]
            if i == 5:
                self.board[i].sides[1].tile = self.board[0]    

# establishing the ports
        random.shuffle(self.ports)
        ports = []
        for i in self.ports:
            ports.extend(i)
        number = 0
        for i in range(6, 17):
            self.board[i].sides[2].tile  = ports[number]
            number += 1
            if i % 2 == 0:
                self.board[i].sides[3].tile  = ports[number]
                number += 1
            self.board[i].sides[4].tile  = ports[number]
            number += 1

# establishing connective nodes on outer tiles

        for i in range(6, 18):
            self.board[i].sides[1].tile = self.board[i + 1]
            self.board[i].sides[5].tile = self.board[i - 1]
            if i == 6:
                self.board[i].sides[5].tile = self.board[17]
            if i == 17:
                self.board[i].sides[1].tile = self.board[6] 
        for i in range(7, 18, 2):   
            self.board[i].sides[0].tile = self.board[int((i - 7) / 2)]
            self.board[i].sides[3].tile = self.board[int((i - 5) / 2)]
            if i == 17:
                self.board[i].sides[3].tile = self.board[0]
                
# sides.adj_side
        for i in self.board:
            for j in range(1, len(i.sides) - 1):
                i.adj_side = [i.sides[j - 1],i.sides[j + 1]]
            i.sides[0].adj_side = [i.sides[5],i.sides[1]]
            i.sides[5].adj_side = [i.sides[4],i.sides[0]]
        for i in self.board[7:17:2]:
            i.sides[1].adj_side = [i.sides[0]]
            i.sides[5].adj_side = [i.sides[3]]
            i.sides[0].adj_side = [i.sides[3],i.sides[1]]
            i.sides[3].adj_side = [i.sides[0],i.sides[5]]
#recursive board creation
    def board_generator(self, starter = False, num = -1):
        random.shuffle(self.tile_types)
        random.shuffle(self.tile_nums)
        
        for i in self.tile_types:
            if self.tile_type[i] != 0:
                for j in self.tile_nums:
                    if self.tile_num[j] != 0:
                        if starter:
                            self.board[num].type = i
                            self.tile_type[i] = self.tile_type.get(i) - 1
                            self.board[num].number = j
                            self.tile_num[j] = self.tile_num.get(j) - 1
                        else:
                            self.board[17].type = i
                            self.tile_type[i] = self.tile_type.get(i) - 1
                            self.board[17].number = j
                            self.tile_num[j] = self.tile_num.get(j) - 1
                        if all(map(lambda foo: foo(self.board[num]), list(self.checks))): ## Check function self.check_all(self.board[num])
                            return self.board_generator(True, num + 1)
        return self.board_generator(True, num - 1)
    def __str__ (self):
        for i in self.board:
            print("" + str(i.tilenum) + " " + str(i.number) + " " + i.type)
        return ""
    
    def alwaysTrue():
         return True
    def two_brone(self, tile2):
        if (tile2.type == "Brick" or tile2.type == "Stone" ):
            for i in range(6):
                if tile2.sides[i].tile.type == tile2.type:
                    return False
        return True




#check functions
# class CheckFunction: 
#     def __init__(self):
#         self.checks = []#[alwaysTrue, two_brone]
#     def check_all(self, tile):
#         lst = all(map(lambda foo: foo(tile), list(self.checks)))
#         return all(lst)
#     def check_add(self, func):
#         self.checks.append[func]
#     def alwaysTrue():
#         return True
#     def two_brone(self, tile2):
#         if (tile2.type == "Brick" or tile2.type == "Stone" ):
#             for i in range(6):
#                 if tile2.sides[i].tile.type == tile2.type:
#                     return False
#         return True
        

        

    

smth = Board()
smth.board_generator()
print(smth)


        # def helper(self, num):
        #     if num == 19:
        #         return self


        # return helper() 
    
        
        