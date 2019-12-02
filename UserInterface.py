import pygame
from math import*
##### File for displaying UI: Health, weapons, character name, boss info #####
class userInterface:
    def __init__(self, game):
        self.game = game
        self.gameAssets = self.game.gameAssets
        self.gameWindow = self.game.gameWindow
        self.wndWidth, self.wndHeight = self.gameWindow.get_size()
        # Make boss healthbar object
        self.bossHP = bossHealthBar(self.gameAssets.allGameImages.healthBarGreen,\
        700, 300, self.wndWidth/2 - 350, self.wndHeight - 150, True, False, self.game)
        self.bossHPTrail = bossHealthBar(self.gameAssets.allGameImages.healthBarRed, \
        700, 100, self.wndWidth/2 - 350, self.wndHeight - 64, True, True, self.game)
        self.bossHPFrame = bossHealthBar(self.gameAssets.allGameImages.HPbossFrame, \
        710, 300, self.wndWidth/2 - 355, self.wndHeight - 145, False, False, self.game)
        # Make player health bar

    # main update method for all user interface
    def update(self):
        self.bossHPTrail.update()
        self.bossHP.update()
        self.bossHPFrame.update()


class bossHealthBar:
    def __init__(self, image, width, height, x, y, isExpansive, isSlow, game):
        # general attributes
        self.isExpansive = isExpansive  #  reacts to damage taken
        self.isSlow = isSlow
        self.width = width
        self.maxWidth = width
        self.height = height
        self.game = game
        self.xpos = x
        self.ypos = y
        self.image = pygame.transform.scale(image, [self.width, self.height])
        self.gameWindow = game.gameWindow
        self.widthCounter = 0

    def update(self):
        # take from boss
        if self.isExpansive:
            self.healthPercent = self.game.allEntities["Hydra"].health \
            / self.game.allEntities["Hydra"].maxHP
            if not self.isSlow:
                # update width
                self.width = ceil(self.maxWidth*self.healthPercent)
            else:
                # make a slow trail
                self.width = ceil(self.maxWidth*self.healthPercent)\
                + self.widthCounter
                if self.widthCounter > 0:
                    self.widthCounter -= 1
            if self.width >= 0:
                self.image = pygame.transform.scale(self.image,\
                [self.width, self.height])
        # draw
        self.gameWindow.blit(self.image, [self.xpos, self.ypos])

    def delayWidth(self, healthPercent):
        self.widthCounter = self.width - ceil(self.maxWidth*healthPercent)

#
## class for player health bar
class playerHealthBar:
    def __init__(self, x, y, width, height, player, imageList):
        self.animationList = []
        self.player = player
        self.x = x
        self.y = y
        self.gameWindow = player.gameWindow
        # our animatinon counter is player health
        for image in imageList:
            self.animationList.append(pygame.transform.scale(image, (width, height)))

    # update health bar
    def update(self):
        # health is index for animation
        self.gameWindow.blit(self.animationList[8  - self.player.health], [self.x, self.y])
