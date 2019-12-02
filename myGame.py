#    15-112: Principles of Programming and Computer Science
#    Final Project : Complexia
#    Name      : Mohammed Al-jawaheri
#    AndrewID  : mjawaher

import pygame
import Menu
import ImageWriter
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
        self.keyUpC = False

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
        if event.type == KEYUP:
            # if player presses C store
            if event.key == pygame.K_c:
                self.keyUpC = not self.keyUpC

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
        self.allCharacterAnimations["fireWizard"] = {}
        self.allCharacterAnimations["lightningMcQueen"] = {}
        self.allCharacterAnimations["fireStaffWizard"] = {}
        self.allCharacterAnimations["Hydra"] = {}
        self.allCharacterAnimations["Minion1"] = {}
        self.allCharacterAnimations["Minion1"]["Idle"] = []
        self.allCharacterAnimations["Player"]["Idle"] = []
        self.allCharacterAnimations["Player"]["Attack1"] = []
        # Boss
        self.allCharacterAnimations["Hydra"]["Idle"] = []
        self.allCharacterAnimations["Hydra"]["rightHand"] = []
        self.allCharacterAnimations["Hydra"]["leftHand"] = []
        # all playable character animations
        # fire character
        self.allCharacterAnimations["fireWizard"]["Idle"] = []
        self.allCharacterAnimations["fireWizard"]["Attack1"] = []
        self.allCharacterAnimations["fireWizard"]["Attack2"] = []
        # lightning character
        self.allCharacterAnimations["lightningMcQueen"]["Idle"] = []
        self.allCharacterAnimations["lightningMcQueen"]["Attack1"] = []
        # fire staff wizard
        self.allCharacterAnimations["fireStaffWizard"]["Idle"] = []
        self.allCharacterAnimations["fireStaffWizard"]["Attack1"] = []
        self.allCharacterAnimations["fireStaffWizard"]["Attack2"] = []
        self.allSpellEffects = {}
        self.allSpellEffects["SkullBolt"] = []
        self.allSpellEffects["Explosion1"] = []
        self.allSpellEffects["PhaseOneBlast"] = []
        self.allSpellEffects["Firecracker"] = []
        self.allSpellEffects["FireBall"] = []
        self.allSpellEffects["CastingSpell"] = []
        self.allSpellEffects["Blizzard"] = []
        self.allSpellEffects["Rain"] = []
        self.playerHealthBar = []
        # load all main game assets
        self.menuBackground = pygame.image.load("Sprite assets\\Backgrounds\\menuBackground.jpg").convert()
        self.gameBackground = pygame.image.load("Sprite Assets\\Backgrounds\\gameBackground.jpg").convert()
        self.mainCharacter = pygame.image.load("Sprite assets\\Characters\\myCharacter.png").convert_alpha()
        self.playButton = pygame.image.load("Sprite Assets\\playButton.jpg").convert_alpha()
        self.platform1 = pygame.image.load("Sprite Assets\\Platforms\platform1.png").convert_alpha()
        self.bossImage = pygame.image.load("Sprite Assets\\Final boss parts\\FinalBoss1.png").convert_alpha()
        self.blackBorder = pygame.image.load("Sprite assets\possible\\blackBorder.png")
        # Load player animations
        for dirName, subdirList, fileList in os.walk("Sprite assets\Animated character\Character2\Move animations Cropped"):
            for fname in sorted(fileList):  # Idle animations
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["Player"]["Idle"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\Animated character\Character2\Attack1 animations Cropped"):
            for fname in sorted(fileList):  # Attack1 animations
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["Player"]["Attack1"].append(pygame.image.load(img_path).convert_alpha())
        # lightning character animations
        for dirName, subdirList, fileList in os.walk("Sprite assets\Animated character\Character1\Move animations Cropped"):
            for fname in sorted(fileList):  # Idle animations
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["lightningMcQueen"]["Idle"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\Animated character\Character1\Attack1 animations Cropped"):
            for fname in sorted(fileList):  # Attack1 animations
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["lightningMcQueen"]["Attack1"].append(pygame.image.load(img_path).convert_alpha())
        # fire wizard animations
        for dirName, subdirList, fileList in os.walk("Sprite assets\Animated character\Character2\Move animations Cropped"):
            for fname in sorted(fileList):  # Idle animations
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["fireWizard"]["Idle"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\Animated character\Character2\Attack1 animations Cropped"):
            for fname in sorted(fileList):  # Attack1 animations
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["fireWizard"]["Attack1"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\Animated character\Character2\Attack2 animations Cropped"):
            for fname in sorted(fileList):  # Attack2 animations
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["fireWizard"]["Attack2"].append(pygame.image.load(img_path).convert_alpha())
        # fire staff wizard animations
        for dirName, subdirList, fileList in os.walk("Sprite assets\Animated character\Character4\Move animations Cropped"):
            for fname in sorted(fileList):  # Idle animations
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["fireStaffWizard"]["Idle"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\Animated character\Character4\Attack1 animations Cropped"):
            for fname in sorted(fileList):  # Attack1 animations
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["fireStaffWizard"]["Attack1"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\Animated character\Character4\Attack2 animations Cropped"):
            for fname in sorted(fileList):  # Attack2 animations
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["fireStaffWizard"]["Attack2"].append(pygame.image.load(img_path).convert_alpha())
        # Load sprite effects
        for dirName, subdirList, fileList in os.walk("Sprite assets\\Final boss parts\\Spell effects\\Boss Spells\\SkullBolt\\Full animation"):
            for fname in sorted(fileList):  # boss skullbolt
                img_path = os.path.join(dirName, fname)
                self.allSpellEffects["SkullBolt"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\\Final boss parts\\Spell effects\\Full explosion1"):
            for fname in sorted(fileList):  # explosion1
                img_path = os.path.join(dirName, fname)
                self.allSpellEffects["Explosion1"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\\Final boss parts\\Spell effects\\Fire Blast"):
            for fname in sorted(fileList):  # fire blast
                img_path = os.path.join(dirName, fname)
                self.allSpellEffects["PhaseOneBlast"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\\Final boss parts\\Spell effects\\firecrack"):
            for fname in sorted(fileList):  # fire cracker
                img_path = os.path.join(dirName, fname)
                self.allSpellEffects["Firecracker"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\Final boss parts\Spell effects\FireBall"):
            for fname in sorted(fileList):  # fire ball
                img_path = os.path.join(dirName, fname)
                self.allSpellEffects["FireBall"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\Final boss parts\Spell effects\castingSpell"):
            for fname in sorted(fileList):  #casting fire
                img_path = os.path.join(dirName, fname)
                self.allSpellEffects["CastingSpell"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\Final boss parts\Spell effects\Blizzard"):
            for fname in sorted(fileList):  # blizzard weather effect
                img_path = os.path.join(dirName, fname)
                self.allSpellEffects["Blizzard"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\Final boss parts\Spell effects\Rain"):
            for fname in sorted(fileList):  # rain weather effect
                img_path = os.path.join(dirName, fname)
                self.allSpellEffects["Rain"].append(pygame.image.load(img_path).convert_alpha())
        # Load minions
        for dirName, subdirList, fileList in os.walk("Sprite assets\Minions\Trash1\Full animations cropped"):
            for fname in sorted(fileList):  # judgement minion
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["Minion1"]["Idle"].append(pygame.image.load(img_path).convert_alpha())
        # Load Idle boss animations
        for dirName, subdirList, fileList in os.walk("Sprite assets\\Final boss Parts\Animated"):
            for fname in sorted(fileList):
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["Hydra"]["Idle"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\\Final boss Parts\leftHand"):
            for fname in sorted(fileList):  # load left hand
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["Hydra"]["leftHand"].append(pygame.image.load(img_path).convert_alpha())
        for dirName, subdirList, fileList in os.walk("Sprite assets\\Final boss Parts\\rightHand"):
            for fname in sorted(fileList):  # load right hand
                img_path = os.path.join(dirName, fname)
                self.allCharacterAnimations["Hydra"]["rightHand"].append(pygame.image.load(img_path).convert_alpha())
        # User interface
        self.healthBarGreen = pygame.image.load("Sprite Assets\\User Interface\\bossHealthBarGreenFinal.png").convert_alpha()
        self.healthBarRed = pygame.image.load("Sprite Assets\\User Interface\\BossHealthBarRed.png").convert_alpha()
        self.HPbossFrame = pygame.image.load("Sprite Assets\\User Interface\\bossFrameTest.png").convert_alpha()
        self.gameOverScreen = pygame.image.load("Sprite Assets\\User Interface\\gameOverScreen.png").convert_alpha()
        self.gameWinScreen = pygame.image.load("Sprite Assets\\User Interface\\gameWinScreen.png").convert_alpha()
        for dirName, subdirList, fileList in os.walk("Sprite assets\\User Interface\\playerHealthBarAnimated"):
            for fname in sorted(fileList):  # player health bar
                img_path = os.path.join(dirName, fname)
                self.playerHealthBar.append(pygame.image.load(img_path).convert_alpha())


# Sources:
# Credit to pixel artist Adam Kling (with personal permission)
# Source: www.spriters-resource.com/snes/magicpopn/sheet/11721/index.html
# https://boingboing.net/2018/09/13/tool-to-create-pixel-art-parti.html
# http://bestanimations.com/Military/Explosions/Explosions2.html#21370
# https://www.animatedimages.org/cat-rain-606.htm
# http://re-lvup.blog.jp/
# https://www.artstation.com/artwork/ZZKVN
# http://pixelartmaker.com/art/98e62e03c812b08
# https://edermunizz.itch.io/free-pixel-art-forest (big thanks to edermunizz)
# UI is my design


#
## Class to load all game sound files
class gameSounds:
    def __init__(self):
        self.menuMusic = pygame.mixer.music.load("sound files\\Login Music.mp3")
        self.buttonPress = pygame.mixer.Sound("sound files\\playButton.wav")
        # https://www.freesoundeffects.com/free-sounds/fireball-10079/ Free for non-commerical use
        self.fireSound1 = pygame.mixer.Sound("sound files\\FireAttackSound.wav")
        self.explosionSound1 = pygame.mixer.Sound("sound files\\fireblastSound.wav")
        self.castingFireSound = pygame.mixer.Sound("sound files\\fireCast.wav")
        self.castingFireSound.set_volume(0.1)
        self.explosionSound1.set_volume(0.090)

        self.musicDictionary = {
            "PhaseOne" : self.startPhaseOne,
            "sadMusic" : self.startSadMusic,
            "chaozAirflow" : self.startChaozAirflow,
            "winMusic" : self.startWinMusic
        }

    def startGameMusic(self):
        self.gameMusic = pygame.mixer.music.load("sound files\BossMusic.wav")
        pygame.mixer.music.play(-1, 0.0)
        return

    def startPhaseOne(self):
        self.gameMusic = pygame.mixer.music.load("sound files\phaseOne.wav")
        pygame.mixer.music.play(-1, 0.0)
        return

    def startSadMusic(self):
        self.gameMusic = pygame.mixer.music.load("sound files\sadMusic.wav")
        pygame.mixer.music.play()
        return

    def startWinMusic(self):
        self.gameMusic = pygame.mixer.music.load("sound files\winMusic.mp3")
        pygame.mixer.music.play()
        return

    def startChaozAirflow(self):
        self.gameMusic = pygame.mixer.music.load("sound files\ChaozAirflow.mp3")
        pygame.mixer.music.play()
        return

    # Call whatever function dictionary with given name refers to
    def shiftPhaseMusic(self, phaseName):
        self.musicDictionary[phaseName]()

#
## pass all game asset objects to this class
class gameAssets:
    def __init__(self, allGameImages, allGameSounds, gameMap, gameWindow):
        self.allGameImages = allGameImages
        self.allGameSounds = allGameSounds
        self.map = gameMap
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


# Fill map according to map image
def setupMap():
    # 1 == platform 0 == nothing
    width = 50
    height = 50
    tileMap = [0] * width
    # fill with zeroes
    for i in range(width):
        tileMap[i] = [0] * height
    myMap = ImageWriter.loadPicture("Sprite assets\Platforms\\mapImageFinal2.png")
    picWidth = ImageWriter.getWidth(myMap)
    picHeight = ImageWriter.getHeight(myMap)
    # go through each pixel
    for x in range(picWidth):
        for y in range(picHeight):
            # if black pixel turn into a 1
            if ImageWriter.getColor(myMap, x, y) == [0, 0, 0]:
                tileMap[x][y] = 1
    return tileMap


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
    allGameAssets = gameAssets(allGameImages, allGameSounds, setupMap(), gameWindow)
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
            if event.type == QUIT:
                gameCleanUp()
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
    #gameCleanUp()
