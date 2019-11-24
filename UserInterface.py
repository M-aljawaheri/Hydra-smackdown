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
        self.bossHP = bossHealthBar(self.gameAssets.allGameImages.healthBarGreen, 700, 100, self.wndWidth/2 - 350, self.wndHeight - 64, True, self.game)
        self.bossHPTrail = bossHealthBar(self.gameAssets.allGameImages.healthBarRed, 700, 100, self.wndWidth/2 - 350, self.wndHeight - 64, True, self.game)
        self.bossHPFrame = bossHealthBar(self.gameAssets.allGameImages.HPbossFrame, 710, 300, self.wndWidth/2 - 355, self.wndHeight - 145, False, self.game)
        # Make player health bar

    # main update method for all user interface
    def update(self):
        self.bossHP.update()
        self.bossHPTrail.update()
        self.bossHPFrame.update()


class bossHealthBar:
    def __init__(self, image, width, height, x, y, isExpansive, game):
        self.isExpansive = isExpansive
        self.width = width
        self.maxWidth = width
        self.height = height
        self.game = game
        self.xpos = x
        self.ypos = y
        self.image = pygame.transform.scale(image, [self.width, self.height])
        self.gameWindow = game.gameWindow

    def update(self):
        # take from boss
        if self.isExpansive:
            healthPercent = self.game.allEntities["Hydra"].health / self.game.allEntities["Hydra"].maxHP
            # update width
            self.width = ceil(self.maxWidth*healthPercent)
            if self.width >= 0 :
                self.image = pygame.transform.scale(self.image, [self.width, self.height])
        # draw
        self.gameWindow.blit(self.image, [self.xpos, self.ypos])
