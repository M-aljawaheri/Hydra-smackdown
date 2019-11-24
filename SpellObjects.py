######## File to manage spells and their objects ########
import pygame
# Spells breakdown :
# When boss casts a spell he creates an object of type spell casted
# Spell object acts as spell and does its job, when spell is finished object is destroyed

#
## All bolt type spells
class boltSpell:
    def __init__(self, x, y, width, height, imageList, speed, target):
        self.target = target
        self.game = target.game
        self.boss = self.game.allEntities["Hydra"]
        self.posVector = pygame.math.Vector2()
        self.posVector.xy = x, y - 200
        self.targetLocation = pygame.Vector2()
        self.targetLocation.xy = target.x, target.y
        self.speed = speed
        self.width = width
        self.height = height
        self.imageList = []
        self.i = 0
        for image in imageList:
            self.imageList.append(pygame.transform.scale(image, (self.width, self.height)))
        # Clock object
        self.clock = pygame.time.Clock()
        self.animationCounter = 0
        self.isExploded = False

    def update(self):
        # Update delta time
        deltaTime = 1 / 60
        # Update target vector
        if self.isExploded is False:
            self.targetLocation.xy = self.target.x, self.target.y
            # Get direction vector (from pos to target)
            directionVector = self.targetLocation - self.posVector
            # Normalize vector retain direction
            directionVector = directionVector.normalize()
            # Update projectile vector
            self.posVector.xy = self.posVector.x + (directionVector.x* self.speed * deltaTime), self.posVector.y + (directionVector.y* self.speed * deltaTime)
            # Detect any physics object collision
            self.detectCollisions()
            self.animate()
            self.draw()
        # If not drawing anymore, update explosion
        else:
            self.childExplosion.update()

    def draw(self):
        if not self.isExploded:
            self.target.gameWindow.blit(self.imageList[self.animationCounter % len(self.imageList)], (self.posVector.x - self.width//2, self.posVector.y - self.width//2))

    def animate(self):
        self.animationCounter += 1

    def isCollide(self, x, y, objectWidth, objectHeight):
        if self.posVector.x >= (x - objectWidth // 2) - self.width // 2 and self.posVector.x <= (x + objectWidth // 2) - self.width // 2:
            if self.posVector.y > (y - objectHeight / 2) - (self.height // 2) and self.posVector.y < y + (objectHeight / 2) - (self.height // 2):
                return True
        return False

    def detectCollisions(self):
        for platform in self.game.platforms:
            if self.isCollide(platform.x, platform.y, platform.width, platform.height):
                # Stop drawing
                self.isExploded = True
                # Make explosion object, explosion object will delete bolt object later
                self.childExplosion = Explosion(self, self.posVector.x, self.posVector.y, 80, 80, self.game.gameAssets.allGameImages.allSpellEffects["Explosion1"], self.game)


    def deleteObject(self):
        self.boss.activeSpells.remove(self)


#
## Explosion objects class
class Explosion:
    def __init__(self, parent, x, y, width, height, imageList, game):
        self.parentSpell = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animationList = []
        self.animationCounter = 0
        self.game = game
        for image in imageList:
            self.animationList.append(pygame.transform.scale(image,
                                     (self.width, self.height)))

    def update(self):
        self.animationCounter += 1
        self.game.gameWindow.blit(self.animationList[self.animationCounter % len(
                                  self.animationList)], (self.x - self.width//2,
                                  self.y - self.height//2))
        if self.animationCounter == len(self.animationList):
            self.parentSpell.deleteObject()




#### Notes:
# I first calculated bolt trajectory with a line equation that updates every frame
# Then i resorted to using vectors,normalizing and increasing by speed*deltatime
# where delta time is 1/FPS
