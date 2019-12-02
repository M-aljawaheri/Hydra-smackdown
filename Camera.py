## This file will handle the camera system
# Camera overview:
# All players pass their coordinates to the camera, the camera will
# make computations and give everyone where things should be drawn
# according to zoom required. camera does not change each object's coordinates
import pygame


#
## Camera manager
class camera:
    def __init__(self, game, x, y):
        self.game = game
        # default target follow
        self.target = game.allEntities["Player"]
        self.boss = game.boss
        # Vectors for camera movement
        self.targetLocation = pygame.Vector2()
        self.targetLocation.xy = self.target.x, self.target.y
        self.posVector = pygame.math.Vector2()
        self.posVector.xy = x, y   # xy coord of camera
        self.bossVec = pygame.Vector2()
        self.wndWidth, self.wndHeight = self.game.gameWindow.get_size()
        self.zoom = 1   # no zooming factor
        self.zoomValues = [1, 0.8, 1.5]
        self.zoomValueLen = len(self.zoomValues)
        self.zoomValueCounter = 0
        self.zoomCounter = 0    # to slow down zooming
        self.speed = 0.003


    # zoom factor > 0 zoom in -- < 0 zoom out
    def relativeToScreen(self, x, y, width, height):
        # take world x coordinates, offset by camera position with window centered around it
        newCoordinates = [(x - self.posVector.x - width//2) * self.getZoomSlowed() + self.wndWidth//2, (y - self.posVector.y - height//2)*self.getZoomSlowed() + self.wndHeight//2]
        return newCoordinates

    # increase or decrease zoom
    def setZoom(self, zoom):
        # this zoom factor will be controlled by the state machine
        self.zoom = zoom

    # change follow target
    def setTarget(self, target):
        self.target = target
        self.boss = self.target.game.boss

    # slowly follow player
    def update(self):
        # update zoom according to button pressed
        self.zoom = self.zoomValues[self.zoomValueCounter % self.zoomValueLen]
        deltaTime = 1/60
        # update target vector
        self.targetLocation.xy = self.target.x, self.target.y
        # update direction
        directionVector = self.targetLocation - self.posVector
        # save distance before normalizing
        distance = directionVector.length()
        # normalize vector
        directionVector.normalize()
        # follow target, multiply by distance to (update camera pos)
        self.posVector.xy = self.posVector.x + (directionVector.x * self.speed * deltaTime * distance), self.posVector.y + (directionVector.y * self.speed * deltaTime * distance)

    def getZoomSlowed(self):
        # if slowed zoom didn't catch up to zoom yet
        if self.zoomCounter != self.zoom:
            # calculator difference
            difference = self.zoom - self.zoomCounter
            # increase slowed zoom by speed*FPS*difference
            self.zoomCounter += 0.01 * 1/60 * difference
            return self.zoomCounter

    def tickZoom(self):
        self.zoomValueCounter += 1
        # re initialize key up
        self.game.gameState.currentInput.keyUpC = False