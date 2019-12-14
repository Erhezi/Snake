# Using A-star searching to solve tha snake game
# For the snake game, the basic rule is to lead a little snake to find and a apple.
# It can be treated as a game to find a path from a current position to other position.
# The snake can has four opions up, down, left and right. The snake is moving following the current direction continuely.
# It cannot turn around without any moving space. That means it terminates the game if choosing the opposite direction.
# That means the snake has three options in each step.
#   Stay at current direction
#   turn a direction which is a perpendicular with the current direction.
#
# Using manhattan distance between a snake head and the apple as h, 
# In the regular case, it should equal to the h_true. but when meeting itself body or other case,
# a snake need a detour, which proves its is admissiable.
# However it can be traped when apple appears at the tail of snake. 
#             up
#             |
#  a  xxxxxxx  - front  
#             |
#             down 
# Three direction h will be equal using manhattan distance. And it choose front always
#
# Change to use max mode, it can do pass it.
#
# The depth of searching is a tricky one.

import collections
from random import random

def decode(state, snake, apple_good_x, apple_good_y, apple_magic_x, apple_magic_y,step):
    iswatchingapple_good, iswatchingapple_magic = False, False
    if any([10000 in row for row in state]):
        index_row_good = [10000 in row for row in state].index(True)
        index_col_good = state[index_row_good].index(10000)
        iswatchingapple_good = True
    
    if any([-10000 in row for row in state]):
        index_row_magic = [-10000 in row for row in state].index(True)
        index_col_magic = state[index_row_magic].index(-10000)
        iswatchingapple_magic=True

    if iswatchingapple_good and iswatchingapple_magic:
        return aStarSearching(snake.x, snake.y, \
            apple_good_x, apple_good_y, \
            apple_magic_x, apple_magic_y, \
            step, snake.direction)
    
    if iswatchingapple_good:
        return aStarSearching(snake.x, snake.y, \
            apple_good_x, apple_good_y, \
            -100, -100, \
            step, snake.direction)

    if random() > 0.1 : return snake.direction
    else:
        if snake.direction == 0:
            return 3
        if snake.direction == 1:
            return 2
        if snake.direction == 2:
            return 0
        if snake.direction == 3:
            return 2

def aStarSearching(snake_x,snake_y, apple_x,apple_y, apple_x_magic, apple_y_magic,step,direction,length):
    snake = [(snake_x[i], snake_y[i]) for i in range(len(snake_x))]
    fronter = collections.defaultdict(int)
    fronter[snake[0]] = GetH(snake[0][0],snake[0][1],apple_x,apple_y)
    exploied = []
    count = 0
    while len(fronter)!= 0:
        print("Fronter: ", fronter, "\n")
        position, h = sorted(fronter.items(), key=lambda t: t[1])[0]
        fronter.pop(position)
        print("pop Fronter: ", position ," h: ", h,"\n")
        # Explored the frintier and  add to explored if not there
        if position not in exploied: exploied.append(position)
        # reach the target return the direction
        if position[0]== apple_x and position[1] == apple_y:
            if count == 0: return direction
            return translateSign(exploied[1][0],exploied[1][1], exploied[0][0], exploied[0][1])

        
        for i in ["x","y"]:
            for j in [-1,1]:
                if i == "x":
                    xnew = position[0]+j*step
                    ynew = position[1]
                if i == "y":
                    ynew = position[1] + j*step
                    xnew = position[0]
                if (xnew, ynew) in snake: continue
                if xnew == apple_x_magic and ynew == apple_y_magic: continue
                if (xnew < 0 or ynew < 0): continue
                if (xnew, ynew) in fronter.keys():
                    fronter[(xnew,ynew)] = min(fronter[(xnew,ynew)], GetH(xnew,ynew,apple_x,apple_y)+count)
                else:
                    fronter[(xnew,ynew)] = GetH(xnew,ynew,apple_x,apple_y) + count
        print("After exploring Current explied:", exploied, "\n")
        count += 1
        if count > length: break
    print("After exploring Current explied:", exploied, "\n")
    if len(exploied)<2: return direction
    return translateSign(exploied[1][0],exploied[1][1], exploied[0][0], exploied[0][1])

    

def GetH (x1,y1,x2,y2):
    # return abs(x1-x2)+abs(y1-y2) # Manhantan
    return max(abs(x1-x2), abs(y1-y2)) # max mode 

def translateSign(x1,y1,hx,hy):
    if x1>hx: 
        print("Selected Right")
        return 0
    if x1<hx:
        print("Selected Left") 
        return 1
    if y1<hy: 
        print("Selected Up")
        return 2
    if y1>hy: 
        print("Selected Down")
        return 3
   

