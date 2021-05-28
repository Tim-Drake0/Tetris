import pygame
import numpy as np
from pygame.locals import *
import math
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

screenSize = (800,600)
screen = pygame.display.set_mode(screenSize, RESIZABLE, 32)

r1 = Rect(520, 400, 160, 40)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    screen.fill(black)
    
    #r1.topright = r1.topright[::-1]
    #r1.bottomleft = r1.topleft[::-1]
    #r1.bottomright = r1.topleft[::-1]
    pygame.draw.rect(screen, red, r1)
    

    pygame.display.flip()

