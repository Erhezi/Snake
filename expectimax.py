# Agent for the snake game to chose a apple to Eat, according to the state given

import numpy as np 
from snake import Snake
import json

p = 0.5
decay = 0.8

with open("12x12_5x5.json","r") as fileResource:
    b= json.load(fileResource)
qtable = b["Qtabel"]



def getSnakelist(snake_x,snake_y):
    return [(snake_x[i],snake_y[i]) for i in range(len(snake_x))]

def expectiMax(snake_x,snake_y, apple_x,apple_y, apple_x_magic, apple_y_magic,step,depth,windowwide,windowhigh,vision_size):
    right, rc = expect(snake_x, snake_y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,0,windowwide,windowhigh,depth,vision_size)
    left, lc = expect(snake_x, snake_y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,1,windowwide,windowhigh,depth,vision_size)
    up, uc = expect(snake_x, snake_y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,2,windowwide,windowhigh,depth,vision_size)
    down, dc = expect(snake_x, snake_y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,3,windowwide,windowhigh,depth,vision_size)
    return np.argmax([right, left, up, down]),rc+lc+uc+dc

def expectiMaxWithQlearning(snake_x,snake_y, apple_x,apple_y, apple_x_magic, apple_y_magic,step,depth,windowwide,windowhigh,vision_size):
    right, rc = expectWithQlearning(snake_x, snake_y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,0,windowwide,windowhigh,depth,vision_size)
    left, lc = expectWithQlearning(snake_x, snake_y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,1,windowwide,windowhigh,depth,vision_size)
    up, uc = expectWithQlearning(snake_x, snake_y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,2,windowwide,windowhigh,depth,vision_size)
    down, dc = expectWithQlearning(snake_x, snake_y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,3,windowwide,windowhigh,depth,vision_size)
    return np.argmax([right, left, up, down]),rc+lc+uc+dc



def expectWithQlearning(snake_x,snake_y, apple_x,apple_y, apple_x_magic, apple_y_magic,step,direction,windowwide,windowhigh,depth,vision_size):
    # update snake
    snake = Snake(length = len(snake_x),step=step)
    snake.x[:] = snake_x[:]
    snake.y[:] = snake_y[:]
    snake.direction = direction
    snake.update(4)

    currentState = encode_ql(snake, apple_x, apple_y, apple_x_magic, apple_y_magic,vision_size,windowwide,windowhigh)
    
    count = 1
    # check to terminate
    snakelist = getSnakelist(snake.x,snake.y)
    # for apple
    if (apple_x,apple_y) in snakelist: 
        if currentState in qtable.keys():
            return max(qtable[currentState]), count
        return 2, count
    if (apple_x_magic,apple_y_magic) in snakelist:
        if np.random.random() < p: 
            if currentState in qtable.keys():
                return max(qtable[currentState]), count
            return 1*p, count
        else: 
            if currentState in qtable.keys():
                return max(qtable[currentState]), count
            return -1, count
    # for boundary
    if any([a< 0 for a in snake.x]): 
        if currentState in qtable.keys():
            return max(qtable[currentState]), count
        return -1, count
    if any([a >= windowwide for a in snake.x]): 
        if currentState in qtable.keys():
            return max(qtable[currentState]), count
        return -1, count
    if any([a< 0 for a in snake.y]): 
        if currentState in qtable.keys():
            return max(qtable[currentState]), count
        return -1, count
    if any([a >= windowhigh for a in snake.y]): 
        if currentState in qtable.keys():
            return max(qtable[currentState]), count
        return -1, count
    # for bit it self
    if any([snakelist[0] == a for a in snakelist[1:]]): 
        if currentState in qtable.keys():
            return max(qtable[currentState]), count
        return -1, count
    if depth == 0: return np.random.random(), count

    right, rc = expect(snake.x,snake.y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,0,windowwide,windowhigh,depth-1,vision_size)
    left, lc = expect(snake.x,snake.y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,1,windowwide,windowhigh,depth-1, vision_size )
    up, uc = expect(snake.x,snake.y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,2,windowwide,windowhigh,depth-1, vision_size )
    down, dc = expect(snake.x,snake.y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,3,windowwide,windowhigh,depth-1, vision_size )
    return decay*(right+left+up+down), count+rc+lc+uc+dc

def expect(snake_x,snake_y, apple_x,apple_y, apple_x_magic, apple_y_magic,step,direction,windowwide,windowhigh,depth,vision_size):
    # update snake
    snake = Snake(length = len(snake_x),step=step)
    snake.x[:] = snake_x[:]
    snake.y[:] = snake_y[:]
    snake.direction = direction
    snake.update(4)

    currentState = encode_ql(snake, apple_x, apple_y, apple_x_magic, apple_y_magic,vision_size,windowwide,windowhigh)
    
    count = 1
    # check to terminate
    snakelist = getSnakelist(snake.x,snake.y)
    # for apple
    if (apple_x,apple_y) in snakelist: 
        return 2, count
    if (apple_x_magic,apple_y_magic) in snakelist:
        if np.random.random() < p: 
            return 1*p, count
        else: 
            return -1, count
    # for boundary
    if any([a< 0 for a in snake.x]): 
        return -1, count
    if any([a >= windowwide for a in snake.x]): 
        return -1, count
    if any([a< 0 for a in snake.y]): 
        return -1, count
    if any([a >= windowhigh for a in snake.y]): 
        return -1, count
    # for bit it self
    if any([snakelist[0] == a for a in snakelist[1:]]): 
        return -1, count
    if depth == 0: return np.random.random(), count

    right, rcount = expect(snake.x,snake.y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,0,windowwide,windowhigh,depth-1,vision_size)
    left, lcount = expect(snake.x,snake.y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,1,windowwide,windowhigh,depth-1, vision_size )
    up, ucount = expect(snake.x,snake.y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,2,windowwide,windowhigh,depth-1, vision_size )
    down, dcount = expect(snake.x,snake.y, apple_x,apple_y, \
        apple_x_magic, apple_y_magic,step,3,windowwide,windowhigh,depth-1, vision_size )
    return decay*(right+left+up+down), count+rcount+lcount+ucount+dcount



def encode_ql(snakeObj, apple_x,apple_y,apple_x_magic,apple_y_magic,vision_size,windowWidth,windowHeight):
        x_head = snakeObj.x[0]
        y_head = snakeObj.y[0]
        snake = [(snakeObj.x[i],snakeObj.y[i]) for i in range(len(snakeObj.x))]
        

        # tail info
        tail_x =  (x_head - snake[-1][0])//snakeObj.step
        tail_y = (y_head-snake[-1][1])//snakeObj.step

        # check distance between snake and apples
        if x_head == apple_x:
            GoodAppleonX = 0
        else:
            GoodAppleonX = (x_head - apple_x)/abs(x_head - apple_x)
        if y_head == apple_y:
            GoodAppleonY = 0
        else:
            GoodAppleonY = (y_head - apple_y)/abs(y_head - apple_y)
        if x_head == apple_x_magic:
            MagicAppleonX = 0
        else:
            MagicAppleonX = (x_head - apple_x_magic)/abs(x_head - apple_x_magic)
        if y_head == apple_y_magic:
            MagicAppleonY = 0
        else:
            MagicAppleonY = (y_head - apple_y_magic)/abs(y_head - apple_y_magic)

        # check wall
        if snakeObj.direction == 0:
            isWall = x_head+vision_size*snakeObj.step >= windowWidth
            istail = (x_head+vision_size*snakeObj.step, y_head) in snake
        if snakeObj.direction == 1:
            isWall = x_head-vision_size*snakeObj.step <= 0
            istail = (x_head-vision_size*snakeObj.step, y_head) in snake
        if snakeObj.direction == 2:
            isWall = y_head-vision_size*snakeObj.step <= 0 
            istail = (x_head,y_head-vision_size*snakeObj.step) in snake
        if snakeObj.direction == 3:
            isWall = y_head+vision_size*snakeObj.step >= windowHeight
            istail = (x_head,y_head+vision_size*snakeObj.step) in snake
        
        return str([snakeObj.direction,GoodAppleonX,GoodAppleonY,MagicAppleonX,MagicAppleonY,isWall,istail,tail_x,tail_y])