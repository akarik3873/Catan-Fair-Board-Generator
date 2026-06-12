import random
import Node_Class
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
        for i in range(19):
            smth = Tile(i)
            self.board.append(smth)
        self.tile_type = {"Wheat": 4, "Sheep": 4, "Wood": 4, "Brick": 3, "Stone": 3, "Desert": 1}
        self.tile_types = ["Wheat", "Sheep", "Wood", "Brick", "Stone", "Desert"] 
        self.tile_num = {2:1, 3:2, 4:2, 5:2, 6:2, 7:1, 8:2, 9:2, 10:2, 11:2, 12:1}
        self.tile_nums = list(range(2, 13))
        self.type_num = {2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", 11:"", 12:""}
        self.history = []
#check functions
        self.smth = CheckFunction()
        # for i in range(19):
        #     self.board[i].tilenum = i
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
                self.board[i].sides[1].tile = self.board[5] # changed 
                self.board[i].sides[2].tile  = self.board[17]
            if i == 5:
                self.board[i].sides[5].tile = self.board[0]    # chnaged 

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
        #print(ports)

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
    def board_generator(self, starter = False, num = 0):
        while num < 19:
            flag = False
            random.shuffle(self.tile_types)
            random.shuffle(self.tile_nums)
            for i in self.tile_types:
                if self.tile_type[i] != 0:
                    for j in self.tile_nums:
                        if self.tile_num[j] != 0:
                    
                            self.board[num].type = i
                            self.board[num].number = j
            
                            if self.smth.check_all(self.board[num]):
                                print("122", num, self.tile_type,self.tile_num )
                                self.smth.type_num[j].append(i)
                                self.tile_num[j] = self.tile_num.get(j) - 1
                                self.tile_type[i] = self.tile_type.get(i) - 1
                                num += 1
                                flag = True
                                break
                        
                if flag==True:
                    break
            else: 
                num = 0
                self.tile_type = {"Wheat": 4, "Sheep": 4, "Wood": 4, "Brick": 3, "Stone": 3, "Desert": 1}
                self.tile_num = {2:1, 3:2, 4:2, 5:2, 6:2, 7:1, 8:2, 9:2, 10:2, 11:2, 12:1}
                self.smth.type_num = [[] for _ in range(13)]

                # print("133", self.tile_type[self.board[num].type],self.tile_num[self.board[num].number])
                # self.tile_type[self.board[num].type] += 1
                # self.tile_num[self.board[num].number] += 1
                # print("136", num, self.tile_type,self.tile_num )
                # num -= 1
                
    

    def __str__ (self):
        for i in self.board:
            print("" + str(i.tilenum) + " " + str(i.number) + " " + i.type)
        return ""



#check functions
class CheckFunction: 
    def __init__(self):
        #input statement 
        self.checks = []
        self.type_num = [[] for _ in range(13)]
        
       
        self.functions1 = [self.two_brone, self.two_num, self.two_sight, self.next_port, self.whoop, self.two_resource, self.sight_resource, self.seven_desert]
        # for i in range(9):
        #     var = input("add?")
        #     if var == "Y":
        #         self.checks.append(self.functions1[i])
    #     check_add = input() 
    #     check_all = input() 
    #     variable_name = input() 
    #     variable_name = input() 
    #     variable_name = input() 
    def check_all(self, tiling):
        lst = map(lambda foo: foo(tiling), list(self.functions1))   #self.checks
        lst = list(lst)
        print('lst:', lst)
        print("all(list(lst))", all(lst))
        return all(lst)
    def check_add(self, func):
        self.checks.append[func]
    def alwaysTrue(self, tile2):
        return True
#two brick and stone next to each other 
    def two_brone(self, tile2):
        if (tile2.type == "Brick" or tile2.type == "Stone"):
            for i in range(6):
                if isinstance(tile2.sides[i].tile, Tile):
                 #   print("172 side type", tile2.sides[i].tile.type, "tile type",tile2.type )
                    if tile2.sides[i].tile.type == tile2.type:
                        return False
        return True
#two six or eight next to each other 
    def two_sight(self, tile2):
        print(tile2.number)
        if (tile2.number == 6 or tile2.number == 8):
            for i in range(6):
                if isinstance(tile2.sides[i].tile, Tile):
                    if tile2.sides[i].tile.number == 6 or tile2.sides[i].tile.number == 8:
                        return False
        return True
#two of the same number next to each other 
    def two_num(self, tile2):
        for i in range(6):
            if isinstance(tile2.sides[i].tile, Tile):
                print(tile2.number)
              #  print("187 side number", tile2.sides[i].tile.number, "tile number",tile2.number)
                if tile2.sides[i].tile.number == tile2.number:
                    return False
        return True
#resource next to its port
    def next_port(self, tile2):
        for i in range(6):
            if tile2.sides[i] == tile2.type:
                return False
        return True
#three wheat, wood, sheep next to each other 
    def whoop(self, tile2):
        counter = 1
        if (tile2.type == "Wood" or tile2.type == "Wheat" or tile2.type == "Sheep"):
            for i in range(6):
                if isinstance(tile2.sides[i].tile, Tile):
                    if tile2.sides[i].tile.type == tile2.type:
                        counter += 1
            if counter > 2:
                return False 
        return True 
#two tiles have the same number and type
    def two_resource(self, tile2):
        if tile2.type in self.type_num[tile2.number]:
            return False
        return True 
#two tiles of same type have mutiple 6 & 8
    def sight_resource(self, tile2):
        if tile2.number == 6 or tile2.number == 8:
            if tile2.type in self.type_num[6] or  tile2.type in self.type_num[8]:
                return False 
        return True
#7 is only on desert
    def seven_desert(self, tile2):
        if tile2.number == 7 and tile2.type != "Desert":
            return False 
        return True
    
        

        
    
    
    
        

        

    



smth = Board()
smth.board_generator()
print(smth)


        # def helper(self, num):
        #     if num == 19:
        #         return self


        # return helper() 
    
        
        