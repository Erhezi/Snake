# Q-learning
# Get some ideals of state from； https://github.com/italohdc/LearnSnake
# State: snakeReletivePostions, GoodAppleReletivePostion, BadAppleReletivePostion

import numpy as np
from collections import defaultdict
import json
from functools import partial


def getRelative(x1, benchmark, step):
    res = x1-benchmark
    while res < 0:
        res += step
    while res > 0:
        res -= step
    return res


class Qlearning:

    def __init__(self, actions, rate=0.8, decayRate=0.7, file = None):

        self.actions = actions
        self.learningRate = rate
        self.decayRate = decayRate
        self.qTable = defaultdict(partial(np.random.rand, len(actions)))
        self.stateCount = defaultdict(partial(np.zeros, len(actions)))
        if file != None:
            with open(file,"r") as fileResource:
                b= json.load(fileResource)
            for k,q in b["Qtabel"].items():
                self.qTable[k]=np.array(q)
            for s, v in b["StatesCounter"].items():
                self.stateCount[s] = np.array(v)

    def getState(self, snake_x, snake_y, magicApple_x, magicApple_y, goodApple_x, goodApple_y, step):
        # head_x = snake_x[0]
        # head_y = snake_y[0]

        # goodApple_x_relative = getRelative(goodApple_x, head_x, step)
        # goodApple_y_relative = getRelative(goodApple_y, head_y, step)
        # magicApple_x_relative = getRelative(magicApple_x, head_x, step)
        # magicApple_y_relative = getRelative(magicApple_y, head_y, step)

        # snakeReletivePostions = []
        # for i in range(len(snake_x)):
        #     tmp_x = getRelative(snake_x[i], head_x, step)
        #     tmp_y = getRelative(snake_y[i], head_y, step)
        #     snakeReletivePostions.append((tmp_x, tmp_y))

        # return (tuple(snakeReletivePostions),
        #         (goodApple_x_relative, goodApple_y_relative),
        #         (magicApple_x_relative, magicApple_y_relative))
        pass

    def updateTable(self, state1, state2, r, act):
        self.stateCount[state1][act] += 1
        learningRate = 1/self.stateCount[state1][act]
        self.qTable[state1][act] += learningRate * \
            (r + self.decayRate*np.max(self.qTable[state2])
             - self.qTable[state1][act])

    def getReward(self, state,act):
        return self.qTable[state][act]

    def getAction(self, state):
        # # many visits = low probability of explore
        # if self.stateCount[state] == 0: self.stateCount[state] = 1
        # explore = (np.random.rand() < self.stateCount[state]**(-1)*20)
        # # explore = (np.random.rand() < self.stateCount[state]>20)
        # if explore:
            
        #     a =  np.random.randint(0,len(self.actions)-1)
        #     print(a)
        #     return a
        return np.argmax(self.qTable[state])

    def translateAgentAction(self, act, direction):
        if direction == 0:
            if act == 0:
                return 2
            if act == 1:
                return 0
            if act == 2:
                return 3
        if direction == 1:
            if act == 0:
                return 0
            if act == 1:
                return 1
            if act == 2:
                return 2
        if direction == 2:
            if act == 0:
                return 1
            if act == 1:
                return 2
            if act == 2:
                return 0
        if direction == 3:
            if act == 0:
                return 0
            if act == 1:
                return 3
            if act == 2:
                return 1

    def translateAppAction(self, act, direction):
        if direction == 0:
            if act == 0:
                return 1
            if act == 2:
                return 0
            if act == 3:
                return 2
        if direction == 1:
            if act == 3:
                return 0
            if act == 1:
                return 1
            if act == 2:
                return 2
        if direction == 2:
            if act == 1:
                return 0
            if act == 2:
                return 1
            if act == 0:
                return 2
        if direction == 3:
            if act == 0:
                return 0
            if act == 3:
                return 1
            if act == 1:
                return 2