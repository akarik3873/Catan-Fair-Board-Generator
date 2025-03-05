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
        for i in range (19):
            smth = Tile(i)
            self.board.append(smth)
        self.tile_type = {"Wheat": 4, "Sheep": 4, "Wood": 4, "Brick": 3, "Stone": 3, "Desert": 1}
        self.tile_types = ["Wheat", "Sheep", "Wood", "Brick", "Stone", "Desert"] 
        self.tile_num = {2:1, 3:2, 4:2, 5:2, 6:2, 7:1, 8:2, 9:2, 10:2, 11:2, 12:1}
        self.tile_nums = list(range(2, 13))
        self.type_num = {2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:"", 11:"", 12:""}
        self.history = []
        for i in range(19):
            self.history += [[]]
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
        print(ports)

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
        smth2 = False 
        counter1 = 0
        
        while num != 19:
            if num < 0:
                num = 0
                print(num)
            flag = False
            random.shuffle(self.tile_types)
            random.shuffle(self.tile_nums)
           # print('109 types:', self.tile_types, '  num', num)
            for i in self.tile_types:
                if self.tile_type[i] != 0:
                    for j in self.tile_nums:
                       # print('118: tile_num  j', j, self.tile_num[j])
                        if self.tile_num[j] != 0:
                            try:
                                self.board[num].type = i
                                #print('115 type', i)
                            except:
                               # print('114: num', num)
                                #raise Exception
                                pass
                            self.board[num].number = j
                                # type_num[ = i
                                # type_num[j] = i
                            #print(self.board[num])
                            
                            if self.smth.check_all(self.board[num]) or (i,j) in self.history[num]: ## Check function self.check_all(self.board[num])fkgjkjghgkh
                                print("137", )
                                self.smth.type_num[j].append(i)
                                self.tile_num[j] = self.tile_num.get(j) - 1
                                self.tile_type[i] = self.tile_type.get(i) - 1
                                self.history[num].append([(i, j)])
                                num += 1
                                flag = True
                                break
                            # else: 
                            #     print("132", num - 1)
                            #     num -= 1
                            #     flag = True
                            #     break
                       # else:
                          #  print('126 else')
                        
                if flag==True:
                    break
            else: 
                print("155", self.tile_type) 
                print("156", self.tile_num) 
                self.tile_type[self.board[num - 1].type] += 1
                self.tile_num[self.board[num - 1].number] += 1
                try:
                    if self.smth.type_num[self.board[num - 1].number] != []:
                        self.smth.type_num[self.board[num - 1].number].pop()
                except:
                    print("160000", self.board[num - 1].number)
                    raise Exception
                self.board[num].type = ""
                self.board[num].number = 0
                print("164", self.tile_type) 
                print("165", self.tile_num) 
                if num == 16:
                    pass
                #print(self)
                print(num)
                num -= 1
                if num < 0:
                    raise Exception
        

        # else:
        #     smth2 = True
        # if smth2 == True:
        #     return self.board_generator(True, num - 1)
    

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
        
       
        self.functions1 = [self.two_brone, self.two_num, self.two_sight, self.next_port, self.whoop, self.central_desert, self.two_resource, self.sight_resource, self.seven_desert]
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
    def two_brone(self, tile2):
        if (tile2.type == "Brick" or tile2.type == "Stone"):
            for i in range(6):
                if isinstance(tile2.sides[i].tile, Tile):
                 #   print("172 side type", tile2.sides[i].tile.type, "tile type",tile2.type )
                    if tile2.sides[i].tile.type == tile2.type:
                        return False
        return True
    def two_sight(self, tile2):
        if (tile2.number == 6 or tile2.number == 8):
            for i in range(6):
                if isinstance(tile2.sides[i].tile, Tile):
                    if tile2.sides[i].tile.type == 6 or tile2.sides[i].tile.type == 8:
                        return False
        return True
    def two_num(self, tile2):
        for i in range(6):
            if isinstance(tile2.sides[i].tile, Tile):
              #  print("187 side number", tile2.sides[i].tile.number, "tile number",tile2.number)
                if tile2.sides[i].tile.number == tile2.number:
                    return False
        return True
    def next_port(self, tile2):
        for i in range(6):
            if tile2.sides[i] == tile2.type:
                return False
        return True
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
    def central_desert(self, tile2):
        ## if tile num != 18, tile type == desert, return false
        if tile2.tilenum != 18 and tile2.type == "Desert":
            print(tile2.tilenum, smth.tile_num)
            return False 
        return True
    def two_resource(self, tile2):
        if self.type_num[tile2.number] == tile2.type:
            return False
        return True 
    def sight_resource(self, tile2):
        if tile2.number == 6 or tile2.number == 8:
            if self.type_num[6] == tile2.type or self.type_num[8] == tile2.type:
                return False 
        return True
    def seven_desert(self, tile2):
        if tile2.number == 7 and tile2.type != "Desert":
            return False 
        return True
    
        

        
    
    
    
        

        

    

smth = Board()
for i in range(100):
    smth = Board()
    smth.board_generator()
    print(smth)


        # def helper(self, num):
        #     if num == 19:
        #         return self


        # return helper() 
    
        
        