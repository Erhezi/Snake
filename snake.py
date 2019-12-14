import pygame
from pygame.locals import *
from random import randint, random
import time
import sys
import json
import numpy as np
from astar import decode, aStarSearching
from qLearning import Qlearning
from collections import defaultdict


class Apple:
    # x position
    # y position
    # step for game move

    def __init__(self, x, y, step):
        self.step = step
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

    def relocate(self, snake):
        self.x = randint(2, 11) * self.step
        self.y = randint(2, 11) * self.step
        while (self.x, self.y) in snake:
            self.x = randint(2, 11) * self.step
            self.y = randint(2, 11) * self.step


class Snake:
    # x is a list of snake position on x
    # y is a list of snake position on y
    # step for game move steps
    # direction: Up, Dowm, Left, and Right
    # length is the snake length, initial as 3

    updateCountMax = 2
    updateCount = 0

    def __init__(self, length, step=20):
        self.length = length
        self.direction = 0
        self.IncreaseFlag = False
        self.DecreaseFlag = False

        # initial positions, no collision.
        self.step = step
        self.x = [0 for i in range(self.length)]
        self.y = [0 for i in range(self.length)]
        self.x[1] = 1*self.step
        self.x[0] = 2*self.step

    def update(self, modele=0):
        if modele == 0:
            self.updateCount = self.updateCount + 1
            if self.updateCount <= self.updateCountMax:
                return

        if self.IncreaseFlag:
            self.Increase()

        elif self.DecreaseFlag:
            self.Decrease()

        else:
            # Regular update previous positions
            for i in range(self.length-1, 0, -1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] += self.step
            if self.direction == 1:
                self.x[0] -= self.step
            if self.direction == 2:
                self.y[0] -= self.step
            if self.direction == 3:
                self.y[0] += self.step

        self.updateCount = 0

    def Increase(self):
        # update position of head of snake
        if self.direction == 0:
            self.x.insert(0, self.x[0]+self.step)
            self.y.insert(0, self.y[0])
        if self.direction == 1:
            self.x.insert(0, self.x[0]-self.step)
            self.y.insert(0, self.y[0])
        if self.direction == 2:
            self.y.insert(0, self.y[0]-self.step)
            self.x.insert(0, self.x[0])
        if self.direction == 3:
            self.y.insert(0, self.y[0]+self.step)
            self.x.insert(0, self.x[0])

        self.length += 1
        self.IncreaseFlag = False
        print(self.x[:self.length])
        print(self.y[:self.length])

    def Decrease(self):
        # update position of head of snake
        if self.length <= 2: 
            self.DecreaseFlag = False
            return

        self.length = randint(2, self.length-1)
        self.x = self.x[:self.length]
        self.y = self.y[:self.length]

        self.DecreaseFlag = False
        print(self.x[:self.length])
        print(self.y[:self.length])

    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3

    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))


class Game:
    def isCollision(self, x1, y1, x2, y2):
        return x1 == x2 and y1 == y2


class App:

    windowWidth = 900
    windowHeight = 800
    snake = None
    apple = 0

    # module for different
    # module 0 is play with a gamer
    # module 1 is play with a random choise
    # modele 2 for a A start
    def __init__(self, module=0, step=20, vision_size = 2, isprint=False, ):
        self._running = True
        self.module = module
        self._display_surf = None
        self._image_surf = None
        self._apple_surf_healthy = None
        self._apple_surf_deathly = None
        self.step = step
        self.game = Game()
        self.snake = Snake(3, step)
        self.apple_healthy = Apple(5, 5, step)
        self.apple_deathly = Apple(10, 10, step)
        self.isprint = isprint
        self.vision_size = vision_size

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            (self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.transform.scale(
            pygame.image.load("snake.png").convert(), (self.step, self.step))
        self._apple_surf_healthy = pygame.transform.scale(
            pygame.image.load("apple.jpg").convert(), (self.step, self.step))
        self._apple_surf_deathly = pygame.transform.scale(
            pygame.image.load("magicapple.png").convert(), (self.step, self.step))

    def appleUpdate(self):
        snake = [(self.snake.x[i],self.snake.y[i]) for i in range(self.snake.length)]
        self.apple_deathly.relocate(snake)
        self.apple_healthy.relocate(snake)
        while self.game.isCollision(self.apple_deathly.x, self.apple_deathly.y, self.apple_healthy.x, self.apple_healthy.y):
            self.apple_healthy.relocate(snake)

    def encode(self):
        # if(self.snake.length < 5):
        #     vision_size = self.snake.length
        # else:
        #     vision_size = 5
        vision_size = self.vision_size
        # currentState = [[0 for row in range(vision_size*2+1)]
        #                 for col in range(vision_size*2+1)]
        currentState = np.zeros((vision_size*2+1,vision_size*2+1))
        x_head = self.snake.x[0]
        y_head = self.snake.y[0]


        # print for snake
        for i in range(self.snake.length):
            if self.snake.x[i]//self.step - x_head//self.step + vision_size >= 0 \
                    and self.snake.x[i]//self.step - x_head//self.step + vision_size < vision_size*2+1 \
                    and self.snake.y[i]//self.step - y_head//self.step + vision_size >= 0 \
                    and self.snake.y[i]//self.step - y_head//self.step + vision_size < vision_size*2+1:

                currentState[self.snake.y[i]//self.step - y_head//self.step + vision_size][self.snake.x[i]//self.step - x_head//self.step + vision_size] \
                    = self.snake.y[i] + self.snake.x[i]

        # check distance between snake and apples
        dist_good_x = abs(x_head - self.apple_healthy.x)//self.step
        if x_head > self.apple_healthy.x:
            dist_good_x *= -1

        dist_good_y = abs(y_head - self.apple_healthy.y)//self.step
        if y_head > self.apple_healthy.y:
            dist_good_y *= -1

        # show the apple if it is at the space
        if dist_good_x + vision_size >= 0 \
            and dist_good_x + vision_size < vision_size*2+1 \
            and dist_good_y + vision_size >= 0 \
            and dist_good_y + vision_size < vision_size*2+1:

            currentState[dist_good_y + vision_size][dist_good_x + vision_size] \
            = 10000

        dist_bad_x = abs(x_head - self.apple_deathly.x)//self.step
        if x_head > self.apple_deathly.x:
            dist_bad_x *= -1

        dist_bad_y = abs(y_head - self.apple_deathly.y)//self.step
        if y_head > self.apple_deathly.y:
            dist_bad_y *= -1

        # show the apple if it is at the space    
        if dist_bad_x + vision_size >= 0 \
            and dist_bad_x + vision_size < vision_size*2+1 \
            and dist_bad_y + vision_size >= 0 \
            and dist_bad_y + vision_size < vision_size*2+1:

            currentState[dist_bad_y + vision_size][dist_bad_x + vision_size] \
            = -10000

        # check the space boundary 
        # If it out space states -1
        for row_index in range(vision_size*2+1):
            if y_head-(vision_size-row_index)*self.step < 0 or \
                y_head-(vision_size-row_index)*self.step >= self.windowHeight:
                for col_index in range(vision_size*2+1):
                    currentState[row_index][col_index] = -1
            else:                
                for col_index in range(vision_size*2+1):
                    if x_head-(vision_size-col_index)*self.step < 0 or \
                        x_head-(vision_size-col_index)*self.step >= self.windowWidth:
                        currentState[row_index][col_index] = -1
            
        if self.isprint:
            for row in currentState:
                print(row)

            print("position for good apple: ", (dist_good_x, dist_good_y),
                  "\npositon for bad apple: ", (dist_bad_x, dist_bad_y))
            print(self.snake.x[:self.snake.length])
            print(self.snake.y[:self.snake.length])
        return np.array2string(currentState)



    def getDistanceOfGoodApple(self):
        return abs(self.snake.x[0]-self.apple_healthy.x)+abs(self.snake.y[0]-self.apple_healthy.y)
    
    def getDistanceOfMagicApple(self):
        return abs(self.snake.x[0]-self.apple_deathly.x)+abs(self.snake.y[0]-self.apple_deathly.y)

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self, agent = None):
        # get state1
        if agent != None: currentState = self.getStateFromAgent(agent)
        distanceGoodApple = self.getDistanceOfGoodApple()
        distanceMagicApple = self.getDistanceOfMagicApple()

        # update case
        self.snake.update(self.module)

        # does snake collide with boundary?
        for i in range(0, self.snake.length):
            if self.snake.x[i] == -100 or (self.snake.x[i] < self.windowWidth and self.snake.x[i] >= 0):
                if self.snake.y[i] == -100 or (self.snake.y[i] < self.windowHeight and self.snake.y[i] >= 0):
                    continue

            # update Q Table
            if agent != None:
                newstate = self.getStateFromAgent(agent)
                agent.updateTable(currentState, newstate, -2, self.snake.direction)

            print("You out of region!")
            print(self.snake.x[:self.snake.length])
            print(self.snake.y[:self.snake.length])
            self._running = False
            return

        # does snake eat apple?
        # eat a healthy apple to grow up
        if self.game.isCollision(self.apple_healthy.x, self.apple_healthy.y, self.snake.x[0], self.snake.y[0]):
            print("Eat a good apple")
            self.appleUpdate()
            self.snake.IncreaseFlag = True
            self.apple += 1

            # update Q Table
            if agent != None:
                newstate = self.getStateFromAgent(agent)
                agent.updateTable(currentState, newstate, 10, self.snake.direction)

        # eat a deathly apple to die
        if self.game.isCollision(self.apple_deathly.x, self.apple_deathly.y, self.snake.x[0], self.snake.y[0]):
            print("Eat a bad apple")
            if(random() > 0.5):
                self.snake.DecreaseFlag = True
                self.appleUpdate()
                # update Q Table
                if agent != None:
                    newstate = self.getStateFromAgent(agent)
                    agent.updateTable(currentState, newstate, 0.8, self.snake.direction)

            else:
                print("You lose! Collision by eatting An apple from the hell")
                # print("You have eaten ", self.apple, " apples")
                # print("x[0] (" + str(self.snake.x[0]) +
                #         "," + str(self.snake.y[0]) + ")")
                # print("apple:", self.apple_deathly.x, ", ", self.apple_deathly.y,"\n")
                if agent != None:
                    newstate = self.getStateFromAgent(agent)
                    agent.updateTable(currentState, newstate, -1, self.snake.direction)
                
                self._running = False
                return

        # does snake collide with itself?
        for i in range(1, self.snake.length):
            if self.game.isCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                print("You lose! Collision by bitting yourself ")
                # print("x[0] (" + str(self.snake.x[0]) +
                #       "," + str(self.snake.y[0]) + ")")
                # print("x[" + str(i) + "] (" + str(self.snake.x[i]) +
                #       "," + str(self.snake.y[i]) + ")")

                if agent != None:
                    newstate = self.getStateFromAgent(agent)
                    agent.updateTable(currentState, newstate, -2, self.snake.direction)
                
                self._running = False
                return

        # regular reward
        if agent != None:
            newstate = self.getStateFromAgent(agent)
            
            r = 0
            if distanceGoodApple > self.getDistanceOfGoodApple():
                r += 0.7
            if distanceGoodApple < self.getDistanceOfGoodApple():
                r -= 0.3
            if distanceMagicApple > self.getDistanceOfMagicApple():
                r += 0.5
            if distanceMagicApple < self.getDistanceOfMagicApple():
                r -= 0.3
            agent.updateTable(currentState, newstate, r, self.snake.direction)
       
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.snake.draw(self._display_surf, self._image_surf)
        self.apple_healthy.draw(self._display_surf, self._apple_surf_healthy)
        self.apple_deathly.draw(self._display_surf, self._apple_surf_deathly)
        pygame.display.flip()

    def getStateFromAgent(self, agent):
        if not agent: return None 
        return self.encode()
        # return agent.getState( self.snake.x, self.snake.y, \
        #     self.apple_deathly.x, self.apple_healthy.y, \
        #     self.apple_healthy.x, self.apple_healthy.y, \
        #     self.step)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self, agent = None, records = None):
        if self.on_init() == False:
            self._running = False

        lifetime = 0
        while(self._running):
            pygame.event.pump()

            if self.module == 0:
                keys = pygame.key.get_pressed()

                if (keys[K_RIGHT]):
                    self.snake.moveRight()

                if (keys[K_LEFT]):
                    self.snake.moveLeft()

                if (keys[K_UP]):
                    self.snake.moveUp()

                if (keys[K_DOWN]):
                    self.snake.moveDown()

                if (keys[K_ESCAPE]):
                    self._running = False

            else:
                select = 0
                if self.module == 1: # direct using A-star Searching
                    select = aStarSearching(self.snake.x, self.snake.y, \
                                self.apple_healthy.x, self.apple_healthy.y, \
                                self.apple_deathly.x, self.apple_deathly.y, \
                                self.step, self.snake.direction, self.snake.length)
                
                if self.module ==2: # Q Learnin
                    currentState = self.getStateFromAgent(agent)
                    select = agent.getAction(currentState)


                if self.module == 3: # benchmark random chose
                   select = randint(0,3)
                # select = decode(currentState, self.snake, 
                #     self.apple_healthy.x, self.apple_healthy.y, \
                #     self.apple_deathly.x, self.apple_deathly.y, \
                #     self.step)


                if (select == 0):
                    self.snake.moveRight()

                if (select == 1):
                    self.snake.moveLeft()

                if (select == 2):
                    self.snake.moveUp()

                if (select == 3):
                    self.snake.moveDown()

                if (select == 4):
                    self._running = False

            self.on_loop(agent)
            self.on_render()

            lifetime+=1
            time.sleep(10.0 / 1000.0)

        if records: records.append((self.apple,lifetime))
        print("You have eaten ", self.apple, " apples and survive ", lifetime)
        self.on_cleanup()


if __name__ == "__main__":

    module = 0
    isprint = False
    iterflag = False
    itereterRange = 1000
    vision_size = 2
    vision_size_flag = False
    if sys.argv.__len__ != 0:
        for agm in sys.argv:
            if agm == "-a":  # A-star
                module = 1
            if agm == "-p":
                isprint = True
            if agm == "-q": # Qlearning
                module = 2
            if agm == "-i":
                iterflag = True
                continue
            if iterflag:
                itereterRange = int(agm)
                iterflag = False
            if agm == "-vs":
                vision_size_flag = True
                continue
            if vision_size_flag:
                vision_size = int(agm)
                vision_size_flag = False
                continue
            
    if module != 2:
        theApp = App(module, isprint=isprint)
        theApp.on_execute()

    else:
        agent = Qlearning([0,1,2,3])
        records = []
        for i in range(itereterRange):
            print("Iterater: ", i)
            theApp = App(module, isprint=isprint, vision_size=vision_size)
            theApp.on_execute(agent, records)

            # WRITE TO Qtable to FILE
            qtable = defaultdict(list)
            for state, q in agent.qTable.items():
                qtable[state] = q.tolist() 

            qtableWithCount = {"Qtabel": qtable, "StatesCounter": agent.stateCount}
            with open("qTable.json","w") as file:
                json.dump(qtable, file)
            

            # #READ FROM FILE
            # with open('listfile.txt', 'r') as filehandle:
            #     basicList = json.load(filehandle)
        print (apples)
