import pygame
from pygame.locals import *
from random import randint, random
import time
import sys


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

    def relocate(self):
        self.x = randint(2, 9) * self.step
        self.y = randint(2, 9) * self.step


class Snake:
    # x is a list of snake position on x
    # y is a list of snake position on y
    # step for game move steps
    # direction: Up, Dowm, Left, and Right
    # length is the snake length, initial as 3

    updateCountMax = 2
    updateCount = 0

    def __init__(self, length, step = 20):
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
        

    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
            if self.IncreaseFlag:
                self.Increase()

            elif self.DecreaseFlag:
                self.Decrease()

            else:
                # Regular update previous positions
                for i in range(self.length-1,0,-1):
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
            self.x.insert(0,self.x[0]+self.step)
            self.y.insert(0,self.y[0])
        if self.direction == 1:
            self.x.insert(0,self.x[0]-self.step)
            self.y.insert(0,self.y[0])
        if self.direction == 2:
            self.y.insert(0,self.y[0]-self.step)
            self.x.insert(0,self.x[0])
        if self.direction == 3:
            self.y.insert(0,self.y[0]+self.step)
            self.x.insert(0,self.x[0])

        self.length += 1
        self.IncreaseFlag = False
        print(self.x[:self.length])
        print(self.y[:self.length])

    def Decrease(self):
        # update position of head of snake
        self.length = randint(1,self.length-1)
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
    def __init__(self, module=0, step = 20, isprint = False):
        self._running = True
        self.module = module
        self._display_surf = None
        self._image_surf = None
        self._apple_surf_healthy = None
        self._apple_surf_deathly = None
        self.step = step
        self.game = Game()
        self.snake = Snake(3,step)
        self.apple_healthy = Apple(5, 5, step)
        self.apple_deathly = Apple(10, 10, step )
        self.isprint = isprint
       

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
        self.apple_deathly.relocate()
        self.apple_healthy.relocate()

    def getCurrentState(self, vision_size = 2, isprint=True):
        currentState = [[0 for row in range(vision_size*2+1)]
                        for col in range(vision_size*2+1)]
        x_head = self.snake.x[self.snake.length-1]
        y_head = self.snake.y[self.snake.length-1]

        # print for snake
        for i in range(self.snake.length):
            if self.snake.x[i]//self.step - x_head//self.step + vision_size >= 0 \
                and self.snake.x[i]//self.step - x_head//self.step + vision_size < vision_size*2+1 \
                and self.snake.y[i]//self.step - y_head//self.step + vision_size >= 0 \
                and self.snake.y[i]//self.step - y_head//self.step + vision_size < vision_size*2+1 :
                
                currentState[self.snake.y[i]//self.step - y_head//self.step + vision_size]\
                    [self.snake.x[i]//self.step - x_head//self.step + vision_size] \
                     = 1

        # check distance between snake and apples
        dist_good_x = abs(x_head - self.apple_healthy.x)//self.step
        if x_head < self.apple_healthy.x: dist_good_x *= -1

        dist_good_y = abs(y_head - self.apple_healthy.y)//self.step
        if y_head < self.apple_healthy.y: dist_good_y *= -1

        dist_bad_x = abs(x_head - self.apple_deathly.x)//self.step
        if x_head < self.apple_deathly.x: dist_bad_x *= -1

        dist_bad_y = abs(y_head - self.apple_deathly.y)//self.step
        if y_head < self.apple_deathly.y: dist_bad_y *= -1

        if self.isprint:
            for row in currentState:
                print(row)
            
            print("position for good apple: ", (dist_good_x, dist_good_y), "\n positon for bad apple: ", (dist_bad_x, dist_bad_y))
            print(self.snake.x[:self.snake.length])
            print(self.snake.y[:self.snake.length])
        return 
        

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.snake.update()

        # does snake collide with itself?
        for i in range(0, self.snake.length):
            if self.snake.x[i] == -100 or (self.snake.x[i] <= self.windowWidth and self.snake.x[i] >= 0):
                if self.snake.y[i] == -100 or (self.snake.y[i] <= self.windowHeight and self.snake.y[i] >= 0):
                    continue

            print("You out of region!")
            print(self.snake.x[:self.snake.length])
            print(self.snake.y[:self.snake.length])
            exit(0)

        # does snake eat apple?
        for i in range(0, self.snake.length):
            # eat a healthy apple to grow up
            if self.game.isCollision(self.apple_healthy.x, self.apple_healthy.y, self.snake.x[i], self.snake.y[i]):
                print("Eat a good apple")
                self.appleUpdate()
                self.snake.IncreaseFlag=True
                self.apple += 1

            # eat a deathly apple to die
            if self.game.isCollision(self.apple_deathly.x, self.apple_deathly.y, self.snake.x[i], self.snake.y[i]):
                print("Eat a bad apple")
                if(random() > 0.5):
                    self.snake.DecreaseFlag = True
                    self.appleUpdate()
                else:
                    print("You lose! Collision by eatting An apple from the hell")
                    print("You have eaten ")
                    print("x[0] (" + str(self.snake.x[0]) +
                          "," + str(self.snake.y[0]) + ")")
                    print("x[" + str(i) + "] (" + str(self.snake.x[i]
                                                      ) + "," + str(self.snake.y[i]) + ")")

                    exit(0)

        # does snake collide with itself?
        for i in range(1, self.snake.length):
            if self.game.isCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                print("You lose! Collision by bitting yourself ")
                print("x[0] (" + str(self.snake.x[0]) +
                      "," + str(self.snake.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.snake.x[i]) +
                      "," + str(self.snake.y[i]) + ")")
                exit(0)

        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.snake.draw(self._display_surf, self._image_surf)
        self.apple_healthy.draw(self._display_surf, self._apple_surf_healthy)
        self.apple_deathly.draw(self._display_surf, self._apple_surf_deathly)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        selections = [1 for j in range(40)] + [4 for j in range(40)] + [2 for j in range(30)] + [3 for j in range(30)]
        i = 0

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

            if self.module == 1:
                select = selections[i]
                if (select == 1):
                    self.snake.moveRight()
                if (select == 2):
                    self.snake.moveLeft()

                if (select == 3):
                    self.snake.moveUp()

                if (select == 4):
                    self.snake.moveDown()

                if (select == 5):
                    self._running = False

                i += 1
                if i == len(selections):
                    i = 0

            if self.module == 2:
                select = 0
                # select = GetAction()
                if (select == 1):
                    self.snake.moveRight()

                if (select == 2):
                    self.snake.moveLeft()

                if (select == 3):
                    self.snake.moveUp()

                if (select == 4):
                    self.snake.moveDown()

                if (select == 5):
                    self._running = False

            self.on_loop()
            self.on_render()
            self.getCurrentState(2)

            time.sleep(100.0 / 1000.0)
        self.on_cleanup()


if __name__ == "__main__":

    module = 0
    if sys.argv.__len__ != 0:
        for agm in sys.argv:
            if agm == "-r":
                module = 1
            elif agm == "-m":
                module = 2
            if agm == "-p":
                isprint = True

    theApp = App(module,isprint=isprint)
    theApp.on_execute()
