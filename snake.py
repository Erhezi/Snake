from random import randint
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
        self.x = [80 for i in range(self.length)]
        self.y = [120 for i in range(self.length)]
        self.x[1] += 1*self.step
        self.x[0] += 2*self.step

    def update(self, modele=0):
        if modele == 0:
            self.updateCount = self.updateCount + 1
            if self.updateCount <= self.updateCountMax:
                return

        if self.IncreaseFlag:
            for i in range(2):
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

