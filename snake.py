import pygame
from pygame.locals import *
from random import randint
import time
 
class Apple:
    x = 0
    y = 0
    step = 44
 
    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 

    def relocate(self):
        self.x = randint(2,9) * self.step
        self.y = randint(2,9) * self.step

 
class Player:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length):
       self.length = length
       for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)
 
       # initial positions, no collision.
       self.x[1] = 1*44
       self.x[2] = 2*44
    #    self.y[1] = 0
    #    self.y[2] = 0
 
    def update(self):
 
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
 
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
 
            self.updateCount = 0
 
 
    def moveRight(self):
        self.direction = 0
 
    def moveLeft(self):
        self.direction = 1
 
    def moveUp(self):
        self.direction = 2
 
    def moveDown(self):
        self.direction = 3 
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        return x1 >= x2 and x1 <= x2 + bsize and y1 >= y2 and y1 <= y2 + bsize
 
class App:
 
    windowWidth = 800
    windowHeight = 600
    player = 0
    apple = 0
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf_healthy = None
        self._apple_surf_deathly = None
        self.game = Game()
        self.player = Player(3) 
        self.apple_healthy = Apple(5,5)
        self.apple_deathly = Apple(10,10)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.transform.scale(pygame.image.load("snakehead.jpg").convert(), (44,44))
        self._apple_surf_healthy = pygame.transform.scale(pygame.image.load("apple.jpg").convert(), (44,44))
        self._apple_surf_deathly = pygame.transform.scale(pygame.image.load("magicapple.png").convert(), (44,44))
        
    def appleUpdate(self):
        self.apple_deathly.relocate()
        self.apple_healthy.relocate()
        
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        self.player.update()

         # does snake collide with itself?
        for i in range(0,self.player.length):
            if self.player.x[i]==-100 or self.player.x[i] <= self.windowWidth and self.player.x[i] >= 0 :
                if self.player.y[i]==-100 or (self.player.y[i] <= self.windowHeight and self.player.y[i] >= 0):
                    continue;
            
            print("You out of region!")
            exit(0)


        
        # does snake eat apple?
        for i in range(0,self.player.length):
            # eat a healthy apple to grow up
            if self.game.isCollision(self.apple_healthy.x,self.apple_healthy.y,self.player.x[i], self.player.y[i],44):
                self.appleUpdate()
                self.player.length += 1
                self.apple += 1

            # eat a deathly apple to die
            if self.game.isCollision(self.apple_deathly.x,self.apple_deathly.y,self.player.x[i], self.player.y[i],44):
                if(randint(0,10) > 6):
                    self.player.length = randint(1, self.player.length-1)
                    self.appleUpdate()
                else:
                    print("You lose! Collision by eatting An apple from the hell")
                    print("You have eaten ")
                    print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                    print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                    
                    exit(0)
            
        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],40):
                print("You lose! Collision by bitting yourself ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                exit(0)

        # self.appleUpdate()
                 
        pass
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple_healthy.draw(self._display_surf, self._apple_surf_healthy)
        self.apple_deathly.draw(self._display_surf, self._apple_surf_deathly)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
 
            if (keys[K_RIGHT]):
                self.player.moveRight()
 
            if (keys[K_LEFT]):
                self.player.moveLeft()
 
            if (keys[K_UP]):
                self.player.moveUp()
 
            if (keys[K_DOWN]):
                self.player.moveDown()
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
 
            time.sleep (50.0 / 1000.0);
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()