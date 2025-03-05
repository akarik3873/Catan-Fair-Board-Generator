# takes in promts 
# creates list of checks 
# if all checks pass, tile is added 

import Random_Board_without_Center_Desert as woCD
import Random_Board_with_Center_Desert as wCD
var = input("center desert?")
if var == "Y":
    smth = wCD.Board()
    smth.board_generator()
    print(smth, "18 7 Desert")
    print(smth.ports)
else:
    smth = woCD.Board()
    smth.board_generator()
    print(smth)
    print(smth.ports)


# six and eight are next to each other 
# ports are cooked 
# same number next to each other 
    