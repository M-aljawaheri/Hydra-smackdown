#    15-112: Principles of Programming and Computer Science
#    Final Project : Complexia
#    Name      : Mohammed Al-jawaheri
#    AndrewID  : mjawaher

import pygame
import Menu
import os
import physics
from pygame.locals import *

#### "constants" for colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
FPS = 60


#
## Class to handle all user input
class inputHandling():
    def __init__(self):
        self.runState = True
        self.mouseX = 0
        self.mouseY = 0
        self.mouseClicked = False
        self.keysPressed = []

    ## update mouse input
    def updateMouseState(self, event):
        # if player quits, break while condition
        if event.type == pygame.QUIT:
            self.runState = False
        # if player moves mouse track movement
        elif event.type == MOUSEMOTION:
            self.mouseX, self.mouseY = pygame.mouse.get_pos()
        # if player clicks, track movement and track click state
        elif event.type == MOUSEBUTTONUP:
            self.mouseX, self.mouseY = pygame.mouse.get_pos()
            self.mouseClicked = True

    ## Get mouse position
    def getMousePos(self):
        return (self.mouseX, self.mouseY)

    ## get mosue click status
    def isMouseClicked(self):
        return self.mouseClicked

    ## Get all keys pressed
    def updateKey(self, event):
        if event.type == KEYDOWN or event.type == KEYUP:
            self.keysPressed = pygame.key.get_pressed()

    ## Get keys from object
    def getKeyPressed(self):
        return self.keysPressed


#
## Class to load all game images in initialization
class gameImages:
    def __init__(self):
        # Dictionary of dictionaries holds all animations for all characters
        self.allCharacterAnimations = {}  # key->unit name, value-> dictionary
        self.allCharacterAnimations["Player"] = {}  # key->attkname,val->imglist
        self.allCharacterAnimations["Hydra"] = {}
        self.allCharacterAnimations["Player"]["Idle"] = []
        self.allCharacterAnimations["Player"]["Attack1"] = []
        self.allCharacterAnimations["Hydra"]["Idle"] = []
        self.allSpellEffects = {}
        self.allSpellEffects["SkullBolt"] = []
        self.allSpellEffects["Explosion1"] = []
        self.menuBackground = pygame.image.load("Sprite assets\\Backgrounds\\menuBackground.jpg")
        self.gameBackground = pygame.image.load("Sprite Assets\\Backgrounds\\gameBackground.jpg")
        self.mainCharacter = pygame.image.load("Sprite assets\\Characters\\myCharacter.png")
        self.playButton = pygame.image.load("Sprite Assets\\playButton.jpg")
        self.platform1 = pygame.image.load("Sprite Assets\\Platforms\platform1.png")
        self.bossImage = pygame.image.load("Sprite Assets\\Final boss parts\\FinalBoss1.png")
        # Load player animations
        for dirName, subdirList, fileList in os.walk("Sprite assets\Animated character\Character2\Move animations Cropped"):
            for fname in sorted(fileList):  # Idle animations
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["Player"]["Idle"].append(pygame.image.load(img_path))
        for dirName, subdirList, fileList in os.walk("Sprite assets\Animated character\Character2\Attack1 animations Cropped"):
            for fname in sorted(fileList):  # Attack animations
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["Player"]["Attack1"].append(pygame.image.load(img_path))
        # Load sprite effects
        for dirName, subdirList, fileList in os.walk("Sprite assets\\Final boss parts\\Spell effects\\Boss Spells\\SkullBolt\\Full animation"):
            for fname in sorted(fileList):  # boss skullbolt
                img_path = os.path.join(dirName, fname)
                self.allSpellEffects["SkullBolt"].append(pygame.image.load(img_path))
        for dirName, subdirList, fileList in os.walk("Sprite assets\\Final boss parts\\Spell effects\\Full explosion1"):
            for fname in sorted(fileList):  # explosion1
                img_path = os.path.join(dirName, fname)
                self.allSpellEffects["Explosion1"].append(pygame.image.load(img_path))
        # Load Idle boss animations
        for dirName, subdirList, fileList in os.walk("Sprite assets\\Final boss Parts\Animated"):
            for fname in sorted(fileList):
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["Hydra"]["Idle"].append(pygame.image.load(img_path))
        # User interface
        self.healthBarGreen = pygame.image.load("Sprite Assets\\User Interface\\bossHealthBarGreenFinal.png")
        self.healthBarRed = pygame.image.load("Sprite Assets\\User Interface\\BossHealthBarRed.png")
        self.HPbossFrame = pygame.image.load("Sprite Assets\\User Interface\\bossFrameTest.png")
# Sources:
# Credit to pixel artist Adam Kling (with personal permission)
# Source: www.spriters-resource.com/snes/magicpopn/sheet/11721/index.html
# https://boingboing.net/2018/09/13/tool-to-create-pixel-art-parti.html
# UI is my design


#
## Class to load all game sound files
class gameSounds:
    def __init__(self):
        self.menuMusic = pygame.mixer.music.load("sound files\World of Warcraft Login Music.mp3")
        self.buttonPress = pygame.mixer.Sound("sound files\playButton.wav")
        # https://www.freesoundeffects.com/free-sounds/fireball-10079/ Free for non-commerical use
        self.fireSound1 = pygame.mixer.Sound("sound files\FireAttackSound.wav")
        return

    def startGameMusic(self):
        self.gameMusic = pygame.mixer.music.load("sound files\BossMusic.wav")
        pygame.mixer.music.play(-1, 0.0)
        return


#
## pass all game asset objects to this class
class gameAssets:
    def __init__(self, allGameImages, allGameSounds, gameWindow):
        self.allGameImages = allGameImages
        self.allGameSounds = allGameSounds
        self.gameWindow = gameWindow


#
## make only big classes global
class gameStates:
    def __init__(self, currentInput, currentState):
        self.currentInput = currentInput
        self.currentState = currentState


# Define in global space
allGameStates = None
allGameAssets = None


#
## Initialization code
def InitializeMyGame():
    pygame.init()
    # cap fps at 60
    fpsClock = pygame.time.Clock()
    fpsClock.tick(FPS)
    # Game window is main display surface
    gameWindow = pygame.display.set_mode((1300, 750))
    pygame.display.set_caption("Complexia")
    # initialize images and sounds objects
    global allGameAssets
    global allGameStates
    allGameImages = gameImages()
    allGameSounds = gameSounds()
    # All game assets and states are globals to be used by other files
    allGameAssets = gameAssets(allGameImages, allGameSounds, gameWindow)
    allGameStates = gameStates(None, None)
    # play background menu music
    pygame.mixer.music.play(-1, 0.0)
    return gameWindow


#
## game loop
def myGameLoop(gameWindow):
    # Current state points at current object of corresponding logic
    global allGameStates
    allGameStates.currentState = Menu.gameIntro(gameWindow,
                                                allGameAssets, allGameStates)
    allGameStates.currentInput = inputHandling()
    # Start game loop
    while allGameStates.currentInput.runState is True:
        # Event handling loop. store events in controller
        for event in pygame.event.get():
            # Mouse events handling
            if event.type == MOUSEMOTION or event.type == MOUSEBUTTONUP:
                allGameStates.currentInput.updateMouseState(event)
            # key board event handling
            allGameStates.currentInput.updateKey(event)
        # update whatever functionality of the object currentstate refers to
        allGameStates.currentState.update()
        pygame.display.update()     # Update the pygame display surface
        # Increment time in physics simulation to next moment
        physics.world.Step(physics.timeStep, physics.vel_iters,
                           physics.pos_iters)
        physics.world.ClearForces()  # Reset forces in physics simulation


#
## clean up code
def gameCleanUp():
    pygame.quit()


#
## for import clash ##
if __name__ == "__main__":
    myGameLoop(InitializeMyGame())
    gameCleanUp()
