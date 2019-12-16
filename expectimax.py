# Agent for the snake game to chose a apple to Eat, according to the state given

from astar import *
import numpy as np 

def expectedMax(snake_x,snake_y, apple_x,apple_y, apple_x_magic, apple_y_magic,step,direction,depth):
    
    goodoperation, rewardG = aStarSearching(snake_x,snake_y, apple_x,apple_y,step,direction,4)
    magicoperation, rewardM = aStarSearching(snake_x,snake_y, apple_x_magic,apple_y_magic,step,direction,4)
    

    return action

