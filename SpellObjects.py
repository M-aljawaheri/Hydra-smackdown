######## File to manage spells and their objects ########
import pygame
# Spells breakdown :
# When boss casts a spell he creates an object of type spell casted
# Spell object acts as spell and does its job, when spell is finished object is destroyed

#
## All bolt type spells
class boltSpell:
    def __init__(self, x, y, width, height, imageList, speed, target, explosionName):
        # General attributes
        self.target = target
        self.game = target.game
        self.camera = self.game.camera
        self.boss = self.game.allEntities["Hydra"]
        self.explosionName = explosionName
        self.posVector = pygame.math.Vector2()
        self.posVector.xy = x, y - 200
        self.targetLocation = pygame.Vector2()
        self.targetLocation.xy = target.x, target.y
        self.speed = speed
        self.width = width
        self.height = height
        self.imageList = []
        # Scale animation list
        for image in imageList:
            self.imageList.append(pygame.transform.scale(image, (self.width, self.height)).convert_alpha())
        # Clock object for getting fps
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
            self.draw()
            self.animate()
        # If not drawing anymore, update explosion
        else:
            self.childExplosion.update()

    # draw self
    def draw(self):
        if not self.isExploded:
            drawCoordinates = self.camera.relativeToScreen(self.posVector.x, self.posVector.y, self.width, self.height)
            self.target.gameWindow.blit(self.imageList[self.animationCounter % len(self.imageList)], drawCoordinates)

    # animate self
    def animate(self):
        self.animationCounter += 1

    # verify collisions
    def isCollide(self, x, y, objectWidth, objectHeight):
        # check later why we have to add width not subract ?
        if self.posVector.x >= (x - objectWidth // 2) - self.width // 2 and self.posVector.x <= (x + objectWidth // 2) + self.width // 2:
            if self.posVector.y > (y - objectHeight / 2) - (self.height // 2) and self.posVector.y < y + (objectHeight / 2) + (self.height // 2):
                return True
        return False

    # continously check for collisions
    def detectCollisions(self):
        for platform in self.game.platforms:
            # if collided with platform
            if self.isCollide(platform.x, platform.y, platform.width, platform.height):
                # Stop drawing
                self.isExploded = True
                self.game.gameAssets.allGameSounds.explosionSound1.play()
                # Make explosion object, explosion object will delete bolt object later
                if self.explosionName == "Firecracker":
                    self.childExplosion = Explosion(self, self.posVector.x, self.posVector.y, 160, 160,
                    self.boss.game.gameAssets.allGameImages.allSpellEffects[self.explosionName], 50, self.game)
                    if self.isCollide(self.target.x, self.target.y, self.target.width, self.target.height):
                        self.game.allEntities["Player"].takeDamage(2)
                else:
                    self.childExplosion = Explosion(self, self.posVector.x, self.posVector.y, 80, 80,
                    self.boss.game.gameAssets.allGameImages.allSpellEffects[self.explosionName], 0, self.game)
                    if self.isCollide(self.target.x, self.target.y, self.target.width, self.target.height):
                        self.game.allEntities["Player"].takeDamage(1)

                return
        # if collided with character
        if self.isCollide(self.target.x, self.target.y, self.target.width, self.target.height):
            # Stop drawing
            self.isExploded = True
            self.game.gameAssets.allGameSounds.explosionSound1.play()
            # Make explosion object, explosion object will delete bolt object later
            if self.explosionName == "Firecracker":
                self.childExplosion = Explosion(self, self.posVector.x, self.posVector.y, 160, 160,
                self.boss.game.gameAssets.allGameImages.allSpellEffects[self.explosionName], 50, self.game)
                self.game.allEntities["Player"].takeDamage(2)
            else:
                self.childExplosion = Explosion(self, self.posVector.x, self.posVector.y, 80, 80,
                self.boss.game.gameAssets.allGameImages.allSpellEffects[self.explosionName], 0, self.game)
                self.game.allEntities["Player"].takeDamage(1)
            return

    # del object when done
    def deleteObject(self):
        self.boss.activeSpells.remove(self)


#
## Explosion objects class
class Explosion:
    def __init__(self, parent, x, y, width, height, imageList, msDelay, game):
        self.parentSpell = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animationList = []
        self.animationCounter = 0
        self.game = game
        self.camera = game.camera
        for image in imageList:
            self.animationList.append(pygame.transform.scale(image,
                                    (self.width, self.height)))
        self.msDelay = msDelay
        self.animationLength = len(self.animationList)
        self.timer = pygame.time.get_ticks()
        self.tempTimer = self.timer
    # update explosion
    def update(self):
        # update timer
        self.timer = pygame.time.get_ticks()
        # if animation is done delete the object
        if self.animationCounter == self.animationLength:
            self.parentSpell.deleteObject()
        # ms delay to slow down quick animations
        if self.timer - self.tempTimer > self.msDelay:
            self.animationCounter += 1
            self.tempTimer = self.timer
        # Draw
        drawCoordinates = self.camera.relativeToScreen(self.x, self.y, self.width, self.height)
        self.game.gameWindow.blit(self.animationList[self.animationCounter % self.animationLength],
                                  drawCoordinates)


#
## class for expansive explosions
class expansiveExplosion:
    def __init__(self, parent, x, y, width, height, imageList, game):
        self.parent = parent
        self.game = game
        self.target = self.game.allEntities["Player"]
        self.camera = game.camera
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animationList = []
        self.animationCounter = 0
        self.enlargeCounter = 0
        self.length = len(imageList)
        # scale all pictures in successive sizes
        for i in range(self.length):
            self.animationList.append(pygame.transform.scale(imageList[i], (self.width//self.length * i , self.height//self.length * i)))

    # keep updating blast
    def update(self):
        # check for collision with player
        if self.isCollide(self.target.x, self.target.y, self.target.width, self.target.height):
            self.game.allEntities["Player"].takeDamage(8)
        drawCoordinates = self.camera.relativeToScreen\
        (self.x, self.y, self.width + self.enlargeCounter, self.height\
        + self.enlargeCounter)
        self.game.gameWindow.blit(self.animationList[self.animationCounter % self.length], drawCoordinates)
        # if not at end of animation increment animation
        if self.animationCounter < self.length - 1:
            self.animationCounter += 1
        else:
            # if reached max enlarge stop enlarging
            if self.enlargeCounter < 2000:
                self.animationList[self.length - 1] = pygame.transform.scale(
                                                                        self.animationList[self.length - 1],
                                                                        (self.width + self.enlargeCounter,
                                                                        self.height + self.enlargeCounter))
                self.enlargeCounter += 400
            else:
                self.parent.activeSpells.remove(self)

    # verify collisions
    def isCollide(self, x, y, objectWidth, objectHeight):
        # check later why we have to add width not subract ?
        if self.x >= (x - objectWidth // 2) - (self.width + self.enlargeCounter) // 2 and self.x <= (x + objectWidth // 2) + (self.width + self.enlargeCounter) // 2:
            if self.y > (y - objectHeight // 2) - (self.height + self.enlargeCounter)// 2 and self.y < y + (objectHeight // 2) + (self.height + self.enlargeCounter)// 2:
                return True
        return False
#### Notes:
# I first calculated bolt trajectory with a line equation that updates every frame
# Then i resorted to using vectors,normalizing and increasing by speed*deltatime
# where delta time is 1/FPS
