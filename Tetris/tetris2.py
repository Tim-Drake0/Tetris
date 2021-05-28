import pygame
import numpy as np
from pygame.locals import *
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

screenSize = (400,960)
screen = pygame.display.set_mode(screenSize, RESIZABLE, 32)

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, row , col, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((39,39))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (row, col)

    def update(self):
        #print(self.rect.bottom)
        if self.rect.bottom != screenSize[1] - 1:
            self.rect.y += 40
        else:
            schedule.cancel_job()
        

    def makeTetriminos():
        tetriminos = pygame.sprite.Group()


        return tetriminos
        


matrix = pygame.sprite.Group()
for c in range(0, 400, 40):
        for r in range(0, 960, 40):
            blackBlock = Player(c, r, black)
            matrix.add(blackBlock)
            
L_list = [(-40, 0), (0, 0), (40, 0), (40, -40)]
L_Block = pygame.sprite.Group()
for elem in L_list:
    mino = Player(160 + elem[0], 160 + elem[1], orange)
    L_Block.add(mino)


move = True

# Schedule for every 1 second move the tetrimino down one
moving = schedule.every(1).seconds.do(L_Block.update)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    schedule.run_pending()


    matrix.draw(screen)
        
    L_Block.draw(screen)

    
    # Display the grid lines
    for c in range(0, 400, 40):
        for r in range(0, 960, 40):
            pygame.draw.rect(screen, grid, (c, r, 40, 40), 1)


    pygame.display.flip()
    clock.tick(10)























"""L_Block = Tetrimino([(-40, 0), (0, 0), (40, 0), (40, -40)], orange)
I_Block = Tetrimino([(-40, 0), (0, 0), (40, 0), (80, 0)], teal)
J_Block = Tetrimino([(-40, -40), (-40, 0), (0, 0), (40, 0)], blue)
S_Block = Tetrimino([(0, 0), (-40, 0), (0, -40), (40, -40)], green)
T_Block = Tetrimino([(0, 0), (-40, 0), (40, 0), (0, -40)], purple)
Z_Block = Tetrimino([(-40, -40), (0, -40), (0, 0), (40, 0)], red)
O_Block = Tetrimino([(0, 0), (40, 0), (0, 40), (40, 40)], yellow)"""