import pygame
from pygame.locals import *
import random
import schedule
import copy
import time



pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
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

class Tetromino:
    def __init__(self, left, top, color, pixelSize, rotate):
        self.rect = Rect(left * pixelSize, top * pixelSize, pixelSize, pixelSize)
        self.color = color
        self.pixelSize = pixelSize
        self.r = 1
        self.rotations = rotate
        if self.color == yellow:
                self.nextCenter = (580, 120)
        else:
            self.nextCenter = (600, 160)
class Matrix:
    screenSize = (800, 800)
    pixelSize = 40
    score = 0
    level = -1

    def __init__(self):
        self.width = 400 // self.pixelSize
        self.height = self.screenSize[1] // self.pixelSize
        self.matrix = [[Tetromino(col, row, black, self.pixelSize, (0, 0)) for col in range(self.width)] for row in range(self.height)]
        self.screen = pygame.display.set_mode(self.screenSize, RESIZABLE)
        self.menu = pygame.Surface((300, 300))
        
    # Starting game variables initialized
    def startGame(self):
        L_Rotate = [[(-40, 0), (0, 0), (40, 0), (40, -40)], [(0, -40), (0, 0), (0, 40), (40, 40)], [(-40, 40), (-40, 0), (0, 0), (40, 0)], [(-40, -40), (0, -40), (0, 0), (0, 40)]]
        I_Rotate = [[(-40, 0), (0, 0), (40, 0), (80, 0)], [(40, -40), (40, 0), (40, 40), (40, 80)], [(-40, 40), (0, 40), (40, 40), (80, 40)], [(0, -40), (0, 0), (0, 40), (0, 80)]]
        J_Rotate = [[(40, 0), (0, 0), (-40, 0), (-40, -40)], [(40, -40), (0, -40), (0, 0), (0, 40)], [(40, 40), (40, 0), (0, 0), (-40, 0)], [(-40, 40), (0, 40), (0, 0), (0, -40)]]
        S_Rotate = [[(0, 0), (-40, 0), (0, -40), (40, -40)], [(0, -40), (0, 0), (40, 0), (40, 40)], [(40, 0), (0, 0), (0, 40), (-40, 40)], [(0, 40), (0, 0), (-40, 0), (-40, -40)]]
        T_Rotate = [[(0, 0), (-40, 0), (40, 0), (0, -40)], [(0, -40), (0, 0), (40, 0), (0, 40)], [(40, 0), (0, 0), (0, 40), (-40, 0)], [(0, 40), (0, 0), (-40, 0), (0, -40)]]
        Z_Rotate = [[(40, 0), (0, 0), (0, -40), (-40, -40)], [(40, -40), (40, 0), (0, 0), (0, 40)], [(40, 40), (0, 40), (0, 0), (-40, 0)], [(-40, 40), (-40, 0), (0, 0), (0, -40)]]
        O_Rotate = [[(40, 40), (0, 40), (40, 0), (0, 0)], [(40, 40), (0, 40), (40, 0), (0, 0)], [(40, 40), (0, 40), (40, 0), (0, 0)], [(40, 40), (0, 40), (40, 0), (0, 0)]]

        self.L_Block = (Tetromino(-1, 0, orange, self.pixelSize, L_Rotate), Tetromino(0, 0, orange, self.pixelSize, L_Rotate), Tetromino(1, 0, orange, self.pixelSize, L_Rotate), Tetromino(1, -1, orange, self.pixelSize, L_Rotate))
        self.I_Block = (Tetromino(-1, 0, teal, self.pixelSize, I_Rotate), Tetromino(0, 0, teal, self.pixelSize, I_Rotate), Tetromino(1, 0, teal, self.pixelSize, I_Rotate), Tetromino(2, 0, teal, self.pixelSize, I_Rotate))
        self.J_Block = (Tetromino(1, 0, blue, self.pixelSize, J_Rotate), Tetromino(0, 0, blue, self.pixelSize, J_Rotate), Tetromino(-1, 0, blue, self.pixelSize, J_Rotate), Tetromino(-1, -1, blue, self.pixelSize, J_Rotate))
        self.S_Block = (Tetromino(0, 0, green, self.pixelSize, S_Rotate), Tetromino(-1, 0, green, self.pixelSize, S_Rotate), Tetromino(0, -1, green, self.pixelSize, S_Rotate), Tetromino(1, -1, green, self.pixelSize, S_Rotate))
        self.T_Block = (Tetromino(0, 0, purple, self.pixelSize, T_Rotate), Tetromino(-1, 0, purple, self.pixelSize, T_Rotate), Tetromino(1, 0, purple, self.pixelSize, T_Rotate), Tetromino(0, -1, purple, self.pixelSize, T_Rotate))
        self.Z_Block = (Tetromino(1, 0, red, self.pixelSize, Z_Rotate), Tetromino(0, 0, red, self.pixelSize, Z_Rotate), Tetromino(0, -1, red, self.pixelSize, Z_Rotate), Tetromino(-1, -1, red, self.pixelSize, Z_Rotate))
        self.O_Block = (Tetromino(1, 1, yellow, self.pixelSize, O_Rotate), Tetromino(0, 1, yellow, self.pixelSize, O_Rotate), Tetromino(1, 0, yellow, self.pixelSize, O_Rotate), Tetromino(0, 0, yellow, self.pixelSize, O_Rotate))
        self.Tetromino_List = (self.L_Block, self.I_Block, self.J_Block, self.S_Block, self.T_Block, self.Z_Block, self.O_Block)

        self.nextTetromino = self.getRandTetromino()

    # Updates window 
    def drawBoard(self):
        self.screen.fill(black)
        # Draw pieces on the board
        for row in self.matrix:
            for block in row:
                pygame.draw.rect(self.screen, block.color, block.rect)

        # Display the grid lines
        for c in range(0, 400, self.pixelSize):
            for r in range(0, self.screenSize[1], self.pixelSize):
                pygame.draw.rect(self.screen, grid, (c, r, self.pixelSize, self.pixelSize), 1)

        # Draw next piece
        for index, mino in enumerate(self.nextTetromino):
            pos = mino.rotations[0]
            pygame.draw.rect(self.screen, mino.color, (mino.nextCenter[0] + pos[index][0], mino.nextCenter[1] + pos[index][1], self.pixelSize, self.pixelSize), 0)
            pygame.draw.rect(self.screen, grid, (mino.nextCenter[0] + pos[index][0], mino.nextCenter[1] + pos[index][1], self.pixelSize, self.pixelSize), 1)

        # Printed text
        myfont = pygame.font.SysFont('couriernew', 30)
        nextText = myfont.render('Next', True, (150, 150, 150))
        tetrisText = myfont.render('TETRIS', True, white)
        scoreText = myfont.render(('SCORE: ' + str(self.score)), True, white)
        levelText = myfont.render(('LEVEL: ' + str(self.level)), True, white)
        self.screen.blit(nextText,(580, 80))
        self.screen.blit(tetrisText,(565, 40))
        self.screen.blit(scoreText,(420, 750))
        self.screen.blit(levelText,(420, 700))

        # Draw next piece box
        pygame.draw.rect(self.screen, grid, (520, 80, 200, 160), 2)

    # Returns a deep copy of a random Tetromino from the Tetromino list
    def getRandTetromino(self):
        return random.choice(copy.deepcopy(self.Tetromino_List))

    def addTetromino(self, coord):
        for mino in self.currentTetromino:
            mino.rect.left += coord[0]
            mino.rect.top += coord[1]
            self.matrix[mino.rect.top // self.pixelSize][mino.rect.left // self.pixelSize] = mino        

    # Rotates Tetromino according to which rotate state it is in
    def rotate(self):
        for mino in self.currentTetromino:
            self.matrix[mino.rect.top // self.pixelSize][(mino.rect.left // self.pixelSize)] = Tetromino(mino.rect.left // self.pixelSize, mino.rect.top // self.pixelSize, black, self.pixelSize, (0, 0))
        for index, mino in enumerate(self.currentTetromino):
            if mino.r == 4:
                mino.r = 0
            rotate = mino.rotations[mino.r]
            (mino.rect.left, mino.rect.top) = (self.currentX + rotate[index][0], self.currentY + rotate[index][1])
            self.matrix[mino.rect.top // self.pixelSize][(mino.rect.left // self.pixelSize)] = mino
            mino.r += 1      
        time.sleep(0.2)

    # Move Tetromino down one block
    def moveDown(self):
        for mino in self.currentTetromino:
            if mino.rect.bottom == self.screenSize[1]:
                return
            self.matrix[mino.rect.top // self.pixelSize][(mino.rect.left // self.pixelSize)] = Tetromino(mino.rect.left // self.pixelSize, mino.rect.top // self.pixelSize, black, self.pixelSize, (0, 0))
        for mino in self.currentTetromino:
            if mino.rect.bottom == self.screenSize[1]:
                return
            mino.rect.top += self.pixelSize
            self.matrix[mino.rect.top // self.pixelSize][mino.rect.left // self.pixelSize] = mino
        self.currentY += self.pixelSize
        self.score += 1

    # Move Tetromino left one block
    def moveLeft(self):
        for mino in self.currentTetromino:
            self.matrix[mino.rect.top // self.pixelSize][(mino.rect.left // self.pixelSize)] = Tetromino(mino.rect.left // 40, mino.rect.top // 40, black, self.pixelSize, (0, 0))
        for mino in self.currentTetromino:
            mino.rect.left += -self.pixelSize
            self.matrix[mino.rect.top // self.pixelSize][mino.rect.left // self.pixelSize] = mino
        self.currentX -= self.pixelSize

    # Move Tetromino right one block
    def moveRight(self):
        for mino in self.currentTetromino:
            self.matrix[mino.rect.top // self.pixelSize][(mino.rect.left // self.pixelSize)] = Tetromino(mino.rect.left // 40, mino.rect.top // 40, black, self.pixelSize, (0, 0))
        for mino in self.currentTetromino:
            mino.rect.left += self.pixelSize
            self.matrix[mino.rect.top // self.pixelSize][mino.rect.left // self.pixelSize] = mino
        self.currentX += self.pixelSize

    # Test if the Tetromino has hit the sides
    def hitSides(self):
        for mino in self.currentTetromino:
            if mino.rect.right == 400 or (self.matrix[mino.rect.top // self.pixelSize][(mino.rect.left // self.pixelSize) + 1].color != black and self.matrix[mino.rect.top // self.pixelSize][(mino.rect.left // self.pixelSize) + 1] not in self.currentTetromino):
                return "Right"
            elif mino.rect.left == 0 or (self.matrix[mino.rect.top // self.pixelSize][(mino.rect.left // self.pixelSize) - 1].color != black and self.matrix[mino.rect.top // self.pixelSize][(mino.rect.left // self.pixelSize) - 1] not in self.currentTetromino):
                return "Left"
        return "None"

    # Test if the Tetromino has hit the bottom or another Tetromino
    def hit(self):
        for mino in self.currentTetromino:
            if mino.rect.bottom == self.screenSize[1]:
                return True
            elif self.matrix[(mino.rect.top // self.pixelSize) + 1][mino.rect.left // self.pixelSize].color != black and self.matrix[(mino.rect.top // self.pixelSize) + 1][mino.rect.left // self.pixelSize] not in self.currentTetromino:
                return True
        return False

    # Check for any full rows
    def checkRows(self):
        numLines = 0
        while True:
            for index, row in enumerate(self.matrix):
                colorCount = 0
                for mino in row:
                    if mino.color == black:
                        break
                    colorCount += 1
                    if colorCount == 10:
                        numLines += 1
                        for newRow in range(index, -1, -1):
                            if newRow == 0:
                                break
                            for newMino in self.matrix[newRow - 1]:
                                newMino.rect.top += self.pixelSize
                            self.matrix[newRow] = self.matrix[newRow - 1]   
                if colorCount < 10 and index == 19:
                    if numLines == 1:
                        self.score += 40 * (self.level - 1)
                    elif numLines == 2:
                        self.score += 100 * (self.level - 1)
                    elif numLines == 3:
                        self.score += 300 * (self.level - 1)
                    elif numLines == 4:
                        self.score += 1200 * (self.level - 1)
                    return

            myfont = pygame.font.SysFont('couriernew', 50)
            startText = myfont.render('Start Game', True, green)
            optionsText = myfont.render('Options', True, yellow)
            quitText = myfont.render('Quit', True, red)

            self.menu.blit(startText,(0, 25))
            self.menu.blit(optionsText,(50, 125))
            self.menu.blit(quitText,(100, 225))
            
            pygame.draw.rect(self.menu, white, (0, 0, 300, 300), 3)

            self.screen.blit(self.menu, (200, 200))

            pygame.display.flip()

    # Game loop
    def gameLoop(self):
        self.startGame()
        #thisEvent = Event()
        # Schedule for every 1 second move the Tetromino down one
        schedule.every(1).seconds.do(self.moveDown)

        while True:
            self.level += 1
            self.checkRows()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            # Make current Tetromino the next Tetromino, then get a new next Tetromino       
            self.currentTetromino = self.nextTetromino
            self.nextTetromino = self.getRandTetromino()

            # Add Tetromino to matrix
            self.currentX = 160
            self.currentY = 160
            self.addTetromino((self.currentX, self.currentY))

            while not self.hit():
                schedule.run_pending()
                for event in list(pygame.event.get() + Event.run_ai()):
                    if event.type == QUIT:
                        pygame.quit()

                # Arrow key logic
                if event.type == KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.rotate()
                    if event.key == pygame.K_LEFT and self.hitSides() != "Left":
                        self.moveLeft()
                    if event.key == pygame.K_RIGHT and self.hitSides() != "Right":
                        self.moveRight()
                    if event.key == pygame.K_DOWN and not self.hit():
                        self.moveDown()
                        
                self.drawBoard()

                pygame.display.flip()
                clock.tick(10)

class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key



    def run_ai():
        global counter
        counter += 1
        if counter < 3:
            return []
        counter = 0
        e = Event(pygame.KEYDOWN, pygame.K_UP)
        return [e]

class AI:
    pass

counter = 0
matrix = Matrix()
matrix.gameLoop()