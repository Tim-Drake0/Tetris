import pygame
import numpy as np
from pygame.locals import *
import random
import schedule

pygame.init()

red = (255,0,0)
black = (0,0,0)
orange = (255, 73, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
green = (0, 255, 0)
teal = (0, 255, 255)
blue = (0, 0, 255)
purple = (104, 0, 255)
grid = (40, 40, 40)

screenSize = (400, 960)
screen = pygame.display.set_mode(screenSize, RESIZABLE, 32)
placedMinos = pygame.Surface(screenSize)

clock = pygame.time.Clock()

class Tetrimino(pygame.sprite.Sprite):
    def __init__(self, mino, color):
        pygame.sprite.Sprite.__init__(self)
        self.setMino(mino)
        self.color = color
        self.x = 160
        self.y = 160
        self.r = 0
        self.changey = 0
        self.changex = 0

    # Set list of squares
    def setMino(self, mino):
        self.__mino = mino
    # Get list of squares
    def getMino(self):
        return self.__mino

    # Display tetrimino
    def display(self):
        for part in self.getMino():
            pygame.draw.rect(screen, self.color, (self.x + part[0], self.y + part[1], 40, 40), 0)
            pygame.draw.rect(screen, black, (self.x + part[0], self.y + part[1], 40, 40), 1)

    # Test if the tetrimino has hit the sides
    def hitSides(self):
        mino = self.getMino()
        for square in mino:
            if square[0] + self.x == 360:
                self.changex = 0
                return "Right"
            elif square[0] + self.x == 0:
                self.changex = 0
                return "Left"
        
        return "None"

    # Test if the tetrimino has hit the bottom or another tetrimino
    def hit(self, matrix):
        for part in self.getMino():
            partDown = ((part[1] + self.y + 40) // 40, (part[0] + self.x) // 40)
            if partDown in self.getMino() or partDown[0] > 24:
                continue
            
            if part[1] + self.y == 920:
                self.changey = 0
                return True
            if matrix[partDown] == 1:
                self.changey = 0
                return True
        
        return False
      
    # Update the matrix of RGB values's
    def matrixUpdate(self, matrix):
        for part in self.getMino():
            matrix[(part[1] + self.y) // 40, (part[0] + self.x) // 40] = [self.color]

        return matrix

    # Rotates tetrimino according to which rotate state it is in
    def rotate(self):
        self.r += 1
        mino = self.getMino()
        if self.color == teal:
            if self.r == 1:
                mino[0] = (80, -40)
                mino[1] = (80, 0)
                mino[2] = (80, 40)
                mino[3] = (80, 80)
            elif self.r == 2:
                mino[0] = (-40, 40)
                mino[1] = (0, 40)
                mino[2] = (40, 40)
                mino[3] = (80, 40)
            elif self.r == 3:
                mino[0] = (0, -40)
                mino[1] = (0, 0)
                mino[2] = (0, 40)
                mino[3] = (0, 80)
            elif self.r == 4:
                mino[0] = (-40, 0)
                mino[1] = (0, 0)
                mino[2] = (40, 0)
                mino[3] = (80, 0)
                self.r = 0

        elif self.color == blue:
            if self.r == 1:
                mino[0] = (40, -40)
                mino[1] = (0, -40)
                mino[2] = (0, 0)
                mino[3] = (0, 40)
            elif self.r == 2:
                mino[0] = (40, 40)
                mino[1] = (40, 0)
                mino[2] = (0, 0)
                mino[3] = (-40, 0)
            elif self.r == 3:
                mino[0] = (-40, 40)
                mino[1] = (0, 40)
                mino[2] = (0, 0)
                mino[3] = (0, -40)
            elif self.r == 4:
                mino[0] = (-40, -40)
                mino[1] = (-40, 0)
                mino[2] = (0, 0)
                mino[3] = (40, 0)
                self.r = 0

        elif self.color == orange:
            if self.r == 1:
                mino[0] = (0, -40)
                mino[1] = (0, 0)
                mino[2] = (0, 40)
                mino[3] = (40, 40)
            elif self.r == 2:
                mino[0] = (40, 0)
                mino[1] = (0, 0)
                mino[2] = (-40, 0)
                mino[3] = (-40, 40)
            elif self.r == 3:
                mino[0] = (0, 40)
                mino[1] = (0, 0)
                mino[2] = (0, -40)
                mino[3] = (-40, -40)
            elif self.r == 4:
                mino[0] = (-40, 0)
                mino[1] = (0, 0)
                mino[2] = (40, 0)
                mino[3] = (40, -40)
                self.r = 0

        elif self.color == yellow:
            # No change
            pass

        elif self.color == green:
            if self.r == 1:
                mino[0] = (0, -40)
                mino[1] = (0, 0)
                mino[2] = (40, 0)
                mino[3] = (40, 40)
            elif self.r == 2:
                mino[0] = (40, 0)
                mino[1] = (0, 0)
                mino[2] = (0, 40)
                mino[3] = (-40, 40)
            elif self.r == 3:
                mino[0] = (0, 40)
                mino[1] = (0, 0)
                mino[2] = (-40, 0)
                mino[3] = (-40, -40)
            elif self.r == 4:
                mino[0] = (0, 0)
                mino[1] = (-40, 0)
                mino[2] = (0, -40)
                mino[3] = (40, -40)
                self.r = 0

        elif self.color == purple:
            if self.r == 1:
                mino[0] = (0, -40)
                mino[1] = (0, 0)
                mino[2] = (40, 0)
                mino[3] = (0, 40)
            elif self.r == 2:
                mino[0] = (40, 0)
                mino[1] = (0, 0)
                mino[2] = (0, 40)
                mino[3] = (-40, 0)
            elif self.r == 3:
                mino[0] = (0, 40)
                mino[1] = (0, 0)
                mino[2] = (-40, 0)
                mino[3] = (0, -40)
            elif self.r == 4:
                mino[0] = (0, 0)
                mino[1] = (-40, 0)
                mino[2] = (40, 0)
                mino[3] = (0, -40)
                self.r = 0

        elif self.color == red:
            if self.r == 1:
                mino[0] = (40, -40)
                mino[1] = (40, 0)
                mino[2] = (0, 0)
                mino[3] = (0, 40)
            elif self.r == 2:
                mino[0] = (40, 40)
                mino[1] = (0, 40)
                mino[2] = (0, 0)
                mino[3] = (-40, 0)
            elif self.r == 3:
                mino[0] = (-40, 40)
                mino[1] = (-40, 0)
                mino[2] = (0, 0)
                mino[3] = (0, -40)
            elif self.r == 4:
                mino[0] = (-40, -40)
                mino[1] = (0, -40)
                mino[2] = (0, 0)
                mino[3] = (40, 0)
                self.r = 0
        
        
        self.setMino(mino)

    def outline(self):
        pass
        """for part in self.getMino():
            distance = 920 + part[1]
            pygame.draw.rect(screen, self.color, (self.x + part[0], distance, 40, 40), 3)"""
            
    def moveDown(self):
        #print(self.rect.bottom)
        self.y += 40


L_Block = Tetrimino([(-40, 0), (0, 0), (40, 0), (40, -40)], orange)
I_Block = Tetrimino([(-40, 0), (0, 0), (40, 0), (80, 0)], teal)
J_Block = Tetrimino([(-40, -40), (-40, 0), (0, 0), (40, 0)], blue)
S_Block = Tetrimino([(0, 0), (-40, 0), (0, -40), (40, -40)], green)
T_Block = Tetrimino([(0, 0), (-40, 0), (40, 0), (0, -40)], purple)
Z_Block = Tetrimino([(-40, -40), (0, -40), (0, 0), (40, 0)], red)
O_Block = Tetrimino([(0, 0), (40, 0), (0, 40), (40, 40)], yellow)

# Used to move the piece down once every second


minoList = [L_Block, I_Block, J_Block, S_Block, T_Block, Z_Block, O_Block]
stationaryMinos = pygame.sprite.Group()
matrix = np.zeros((24, 10))

# Game loop
while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    currentMino = random.choice(minoList.copy())
    currentMino.x = currentMino.y = 160

    # Schedule for every 1 second move the tetrimino down one
    schedule.every(1).seconds.do(currentMino.moveDown)

    # Loop for the current tetrimino being moved
    while not currentMino.hit(matrix):
        
        schedule.run_pending()
        screen.fill(black)
        screen.blit(placedMinos, [0, 0])
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            # Arrow key results
            if event.type == KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_UP]:
                    currentMino.rotate()
                if pygame.key.get_pressed()[pygame.K_LEFT] and currentMino.hitSides() != "Left":
                    currentMino.changex = -40
                if pygame.key.get_pressed()[pygame.K_RIGHT] and currentMino.hitSides() != "Right":
                    currentMino.changex = 40
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    currentMino.changey = 40

            if event.type == KEYUP:
                currentMino.changey = 0
                currentMino.changex = 0
    
        currentMino.y += currentMino.changey
        currentMino.x += currentMino.changex
        
        currentMino.hitSides()
        currentMino.display()
        currentMino.outline()
        
        # Display the grid lines
        for c in range(0, 400, 40):
            for r in range(0, 960, 40):
                pygame.draw.rect(screen, grid, (c, r, 40, 40), 1)

        pygame.display.flip()
        clock.tick(10)
    
    stationaryMinos.add(currentMino)
    print(stationaryMinos)

    # Display tetrimino on different pygame surface
    for part in currentMino.getMino():
        pygame.draw.rect(placedMinos, currentMino.color, (currentMino.x + part[0], currentMino.y + part[1], 40, 40), 0)
        pygame.draw.rect(placedMinos, black, (currentMino.x + part[0], currentMino.y + part[1], 40, 40), 1)

    # Update matrix
    currentMino.matrixUpdate(matrix)

    for row in range(0, 960, 40):
        if matrix[(row // 40)].all() == 1:
            for newRow in range(0, row // 40, 40):
                matrix[newRow + 1] = matrix[newRow]
                if newRow + 1 == row:
                    break
            for c in range(0, 400, 40):
                for r in range(0, 960, 40):
                    print(matrix[r // 40, c // 40])
                    if matrix[r // 40, c // 40] != 0:
                        pygame.draw.rect(placedMinos, matrix[r // 40, c // 40], (c, r, 40, 40), 0)
                        pygame.draw.rect(placedMinos, black, (c, r, 40, 40), 1)



            """print(str(matrix[(row // 40)]) + "\n")
            print("delete line")
            for c in range(0, 400, 40):
                pygame.draw.rect(placedMinos, black, (c, row, 40, 40), 0)
                pygame.draw.rect(placedMinos, grid, (c, row, 40, 40), 1)"""



    pygame.display.flip()