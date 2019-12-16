import pygame
from pygame.locals import *
from random import randint, random
import time
import sys
import json
import numpy as np
from astar import decode, aStarSearching
from snake import Snake
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


class Game:
    def isCollision(self, x1, y1, x2, y2):
        return x1 == x2 and y1 == y2


class App:

    windowWidth = 240
    windowHeight = 240
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
        self.apple_healthy = Apple(randint(0,6), randint(2,5), step)
        self.apple_deathly = Apple(randint(7,10), randint(5,10), step)
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

                currentState[self.snake.y[i]//self.step - y_head//self.step + vision_size][self.snake.x[i]//self.step - x_head//self.step + vision_size] = 1
                #currentState[self.snake.y[i]//self.step - y_head//self.step + vision_size][self.snake.x[i]//self.step - x_head//self.step + vision_size] = self.snake.y[i] + self.snake.x[i]

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
        
        return "Version space: "+ np.array2string(currentState)
        # return "Version space: "+ np.array2string(currentState) + " CurrentDirection: "+ str(self.snake.direction)



    def encode_ql(self):
        x_head = self.snake.x[0]
        y_head = self.snake.y[0]
        snake = [(self.snake.x[i],self.snake.y[i]) for i in range(len(self.snake.x))]
        vision_size = self.vision_size

        # tail info
        tail_x =  (x_head - snake[-1][0])//self.step
        tail_y = (y_head-snake[-1][1])//self.step

        # check distance between snake and apples
        if x_head == self.apple_healthy.x:
            GoodAppleonX = 0
        else:
            GoodAppleonX = (x_head - self.apple_healthy.x)/abs(x_head - self.apple_healthy.x)
        if y_head == self.apple_healthy.y:
            GoodAppleonY = 0
        else:
            GoodAppleonY = (y_head - self.apple_healthy.y)/abs(y_head - self.apple_healthy.y)
        if x_head == self.apple_deathly.x:
            MagicAppleonX = 0
        else:
            MagicAppleonX = (x_head - self.apple_deathly.x)/abs(x_head - self.apple_deathly.x)
        if y_head == self.apple_deathly.y:
            MagicAppleonY = 0
        else:
            MagicAppleonY = (y_head - self.apple_deathly.y)/abs(y_head - self.apple_deathly.y)

        # check wall
        if self.snake.direction == 0:
            isWall = x_head+vision_size*self.step >= self.windowWidth
            istail = (x_head+vision_size*self.step, y_head) in snake
        if self.snake.direction == 1:
            isWall = x_head-vision_size*self.step <= 0
            istail = (x_head-vision_size*self.step, y_head) in snake
        if self.snake.direction == 2:
            isWall = y_head-vision_size*self.step <= 0 
            istail = (x_head,y_head-vision_size*self.step) in snake
        if self.snake.direction == 3:
            isWall = y_head+vision_size*self.step >= self.windowHeight
            istail = (x_head,y_head+vision_size*self.step) in snake
        
        return str([self.snake.direction,GoodAppleonX,GoodAppleonY,MagicAppleonX,MagicAppleonY,isWall,istail,tail_x,tail_y])
        # return "Version space: "+ np.array2string(currentState) + " CurrentDirection: "+ str(self.snake.direction)

    def encode_forTree(self):
        x_head = self.snake.x[0]
        y_head = self.snake.y[0]
        snake = [(self.snake.x[i],self.snake.y[i]) for i in range(len(self.snake.x))]
        vision_size = self.vision_size

        # check distance between snake and apples
        if x_head == self.apple_healthy.x:
            GoodAppleonX = 0
        else:
            GoodAppleonX = (x_head - self.apple_healthy.x)/abs(x_head - self.apple_healthy.x)
        if y_head == self.apple_healthy.y:
            GoodAppleonY = 0
        else:
            GoodAppleonY = (y_head - self.apple_healthy.y)/abs(y_head - self.apple_healthy.y)
        if x_head == self.apple_deathly.x:
            MagicAppleonX = 0
        else:
            MagicAppleonX = (x_head - self.apple_deathly.x)/abs(x_head - self.apple_deathly.x)
        if y_head == self.apple_deathly.y:
            MagicAppleonY = 0
        else:
            MagicAppleonY = (y_head - self.apple_deathly.y)/abs(y_head - self.apple_deathly.y)

        isobstrack = False
        # check wall
        if self.snake.direction == 0:
            if x_head+self.step >= self.windowWidth:
                isobstrack = True 
            else:
                if x_head+self.step in self.snake.x:
                    isobstrack = any([(x_head+self.step,y_head+i*self.step) in snake for i in range(-vision_size,vision_size+1)])

        if self.snake.direction == 1:
            if x_head-self.step <= 0:
                isobstrack = True 
            else:
                if x_head-self.step in self.snake.x:
                    isobstrack = any([(x_head-self.step,y_head+i*self.step) in snake for i in range(-vision_size,vision_size+1)])
        if self.snake.direction == 2:
            if y_head-self.step <= 0:
                isobstrack = True 
            else:
                if y_head-self.step in self.snake.y:
                    isobstrack = any([(x_head+i*self.step,y_head-self.step) in snake for i in range(-vision_size,vision_size+1)])
        if self.snake.direction == 3:
            if y_head+self.step >= self.windowHeight:
                isobstrack = True 
            else:
                if y_head+self.step in self.snake.y:
                    isobstrack = any([(x_head+i*self.step,y_head+self.step) in snake for i in range(-vision_size,vision_size+1)])
        
        return str([self.snake.direction,GoodAppleonX,GoodAppleonY,MagicAppleonX,MagicAppleonY,isobstrack])
        # return "Version space: "+ np.array2string(currentState) + " CurrentDirection: "+ str(self.snake.direction)



    def getDistanceOfGoodApple(self):
        return abs(self.snake.x[0]-self.apple_healthy.x)+abs(self.snake.y[0]-self.apple_healthy.y)
    
    def getDistanceOfMagicApple(self):
        return abs(self.snake.x[0]-self.apple_deathly.x)+abs(self.snake.y[0]-self.apple_deathly.y)

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self, select, agent = None):
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
                agent.updateTable(currentState, newstate, -100, select)

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
                agent.updateTable(currentState, newstate, 1000, select)

        # eat a deathly apple to die
        if self.game.isCollision(self.apple_deathly.x, self.apple_deathly.y, self.snake.x[0], self.snake.y[0]):
            print("Eat a bad apple")
            self.apple += 1
            if(random() > 0.5):
                self.snake.DecreaseFlag = True
                self.appleUpdate()
                # update Q Table
                if agent != None:
                    newstate = self.getStateFromAgent(agent)
                    agent.updateTable(currentState, newstate, 100, select)

            else:
                print("You lose! Collision by eatting An apple from the hell")
                # print("You have eaten ", self.apple, " apples")
                # print("x[0] (" + str(self.snake.x[0]) +
                #         "," + str(self.snake.y[0]) + ")")
                # print("apple:", self.apple_deathly.x, ", ", self.apple_deathly.y,"\n")
                if agent != None:
                    newstate = self.getStateFromAgent(agent)
                    agent.updateTable(currentState, newstate, -50, select)
                
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
                    agent.updateTable(currentState, newstate, -120, select)
                
                self._running = False
                return

        # regular reward
        if agent != None:
            newstate = self.getStateFromAgent(agent)
            
            r = 0
            if distanceGoodApple > self.getDistanceOfGoodApple():
                r += 30
            if distanceGoodApple <= self.getDistanceOfGoodApple():
                r -= 20
            if distanceMagicApple > self.getDistanceOfMagicApple():
                r -= 20
            if distanceMagicApple <= self.getDistanceOfMagicApple():
                r += 15
            agent.updateTable(currentState, newstate, r, select)
       
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.snake.draw(self._display_surf, self._image_surf)
        self.apple_healthy.draw(self._display_surf, self._apple_surf_healthy)
        self.apple_deathly.draw(self._display_surf, self._apple_surf_deathly)
        pygame.display.flip()

    def getStateFromAgent(self, agent):
        if not agent: return None 
        return self.encode_ql()
        # return agent.getState( self.snake.x, self.snake.y, \
        #     self.apple_deathly.x, self.apple_healthy.y, \
        #     self.apple_healthy.x, self.apple_healthy.y, \
        #     self.step)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self, agent = None, records = None, statesCounter = None):
        if self.on_init() == False:
            self._running = False

        lifetime = 0
        reward = 0

        while(self._running):
            pygame.event.pump()
            act_agent = 0
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
                    select, _ = aStarSearching(self.snake.x, self.snake.y, \
                                self.apple_healthy.x, self.apple_healthy.y, \
                                self.step, self.snake.direction, 10)
                
                if self.module ==2: # Q Learnin
                    currentState = self.getStateFromAgent(agent)
                    
                    # many visits = low probability of explore
                    statecounter = sum(agent.stateCount[currentState])
                    if statecounter == 0: statecounter = 1
                    explore = (np.random.rand() < statecounter**(-1))
                    if explore:
                        select=  np.random.randint(3)
                        # select = aStarSearching(self.snake.x, self.snake.y, \
                        #         self.apple_healthy.x, self.apple_healthy.y, \
                        #         self.apple_deathly.x, self.apple_deathly.y, \
                        #         self.step, self.snake.direction, self.snake.length)
                    else: 
                        act_agent = agent.getAction(currentState)           
                        select = agent.translateAgentAction(act_agent, self.snake.direction)


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

            self.on_loop(act_agent, agent)
            if self.module == 2:
                reward += agent.getReward(self.getStateFromAgent(agent), act_agent)
            if statesCounter != None:
                statesCounter[self.encode_ql()]+=1
            self.on_render()

            lifetime+=1
            time.sleep(100.0 / 1000.0)

        if records != None: records.append((self.apple,lifetime, reward/lifetime))

        print("You have eaten ", self.apple, " apples and survive ", lifetime)
        self.on_cleanup()


if __name__ == "__main__":

    module = 0
    isprint = False
    iterflag = False
    itereterRange = 1000
    vision_size = 2
    vision_size_flag = False
    file_flag = False
    import_file_flag = False
    filename = "qTable.json"
    if sys.argv.__len__ != 0:
        for agm in sys.argv:
            if agm == "-a":  # A-star
                module = 1
            if agm == "-p":
                isprint = True
            if agm == "-q": # Qlearning
                module = 2
            if agm == "-r":  # benchmark
                module = 3
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
            if agm == "-f":
                file_flag = True
                continue
            if file_flag:
                filename = agm
                file_flag = False
                import_file_flag = True
                continue

    records = []

    if module == 0 or module == 1: #manuly or a start
        theApp = App(module, isprint=isprint)
        theApp.on_execute()

    elif module == 2:
        if import_file_flag:
            agent = Qlearning([0,1,2], file=filename)
        else:
            agent = Qlearning([0,1,2])
        
        for i in range(itereterRange):
            print("Iterater: ", i)
            theApp = App(module, isprint=isprint, vision_size=vision_size)
            theApp.on_execute(agent=agent, records=records)

            # WRITE TO Qtable to FILE
            qtable = defaultdict(list)
            for state, q in agent.qTable.items():
                qtable[state] = q.tolist() 
            statetable = defaultdict(list)
            for state, v in agent.stateCount.items():
                statetable[state] = v.tolist() 

            if i % 10 == 0:
                qtableWithCount = {"Qtabel": qtable, "StatesCounter": statetable}
                with open("qTable.json","w") as file:
                    json.dump(qtableWithCount, file)

        eatapples = [a[0] for a in records]
        lifetimes = [a[1] for a in records]
        rewards = [a[2] for a in records] 
        print ("Game results: ", records,"\n", "Max apples number: ", max(eatapples), "\nMax lifetime: ", max(lifetimes),"\nMax reward: ", max(rewards))
        with open("Result.json", "w") as gameresults:
            json.dump(records,gameresults)

    elif module==3:
        print("Play the game ", itereterRange, "times ramndomly as a benchmark\n")
        statesCounter = defaultdict(int)
        for i in range(itereterRange):
            print("Iterater: ", i)
            theApp = App(module, isprint=isprint, vision_size=vision_size)
            theApp.on_execute(records=records, statesCounter=statesCounter)

            if i % 100 == 0:
                with open("State.json","w") as file:
                    json.dump(statesCounter, file)

        eatapples = [a[0] for a in records]
        lifetimes = [a[1] for a in records]
        # rewards = [a[2] for a in records] 
        print ("Game results: ", records,"\n", "Max apples number: ", max(eatapples), "\nMax lifetime: ", max(lifetimes))
        with open("Result.json", "w") as gameresults:
            json.dump(records,gameresults)
        