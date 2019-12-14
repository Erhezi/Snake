# Q-learning
# Get some ideals of state from； https://github.com/italohdc/LearnSnake/blob/master
# State: snakeReletivePostions, GoodAppleReletivePostion, BadAppleReletivePostion

import numpy as np
from collections import defaultdict
from functools import partial


def getRelative(x1, benchmark, step):
    res = x1-benchmark
    while res < 0:
        res += step
    while res > 0:
        res -= step
    return res


class Qlearning:

    def __init__(self, actions, rate=0.8, decayRate=0.7):

        self.actions = actions
        self.qTable = defaultdict(partial(np.zeros, len(actions)))
        self.stateCount = defaultdict(int)
        self.learningRate = rate
        self.decayRate = decayRate

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
        self.stateCount[state1] += 1
        self.qTable[state1][act] += self.learningRate * \
            (r + self.decayRate*np.max(self.qTable[state2])
             - self.qTable[state1][act])

    def getAction(self, state):
        # many visits = low probability of explore
        if self.stateCount[state] == 0: self.stateCount[state] = 1
        explore = (np.random.rand() < self.stateCount[state]**(-1))
        if explore:
            return np.random.randint(len(self.actions)-1)
        return np.argmax(self.qTable[state])
