import pygame
import gameLogic
from pygame.locals import*

#### "constants" for colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255,   0)
BLUE = (0, 0, 255)
FPS = 60


#
## Game menu class
class gameIntro:
    def __init__(self, gameWindow, gameAssets, allGameState):
        self.gameAssets = gameAssets
        self.allGameStates = allGameState
        self.w, self.h = gameWindow.get_size()
        self.gameWindow = gameWindow
        # initialize buttons
        self.Button1 = Button(gameAssets.allGameImages.playButton, self.w // 2, self.h // 3, self.w // 6, self.h // 4, gameWindow)

    ## Draw on screen
    def update(self):
        self.gameWindow.blit(self.gameAssets.allGameImages.menuBackground, [0, 0])
        self.Button1.draw()
        self.buttonClickCheck()

    ## check current button click
    def buttonClickCheck(self):
        mouseX, mouseY = self.allGameStates.currentInput.getMousePos()
        # if mouse clicked and button collide
        if self.allGameStates.currentInput.mouseClicked:
            if self.Button1.collidepoint(mouseX, mouseY or self.Button2.\
                collidepoint(mouseX, mouseY)):
                # change current state to point to a gamelogic object
                self.allGameStates.currentState = gameLogic.mainGame\
                (self.gameAssets, self.allGameStates, self.gameWindow)
                # play button press sound
                self.gameAssets.allGameSounds.buttonPress.play()
                # change game music
                self.gameAssets.allGameSounds.startGameMusic()


#
## Class to draw menu buttons
class Button:
    def __init__(self, image, x, y, width, height, gameWindow):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        # resize image
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.gameWindow = gameWindow

    ## draw button
    def draw(self):
        self.gameWindow.blit(self.image, [self.x - (self.width//2), self.y - (self.height//2)])

    ## check for collision with button
    def collidepoint(self, x, y):
        if x >= self.x - (self.width//2) and x <= self.x + (self.width // 2):
            if y >= self.y - (self.height//2) and y <= self.y + (self.height //2):
                return True
        return False
