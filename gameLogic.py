import pygame
import physics
import enemyAI
import SpellObjects
import UserInterface
import Camera
# Main game object, will be pointed at by currentState
## update() method continuously updates the game
class mainGame:
    def __init__(self, gameAssets, gameState, gameWindow):
        # All classes access resources e.g assets and window/states from here
        self.gameWindow = gameWindow
        self.gameAssets = gameAssets
        self.map = gameAssets.map
        self.gameState = gameState
        self.platforms = []
        self.allEntities = {}
        self.dead = False
        self.win = False
        # load all characters and inanimate objects as attributes
        self.wndWidth, self.wndHeight = gameWindow.get_size()
        self.initializeCharactersAndObjects()
        self.gameAssets.allGameImages.gameBackground = pygame.transform.scale(self.gameAssets.allGameImages.gameBackground,
                                                                              (self.wndWidth, self.wndHeight))

        self.background = pygame.transform.scale(self.gameAssets.allGameImages.gameBackground, (self.wndWidth, self.wndHeight))
        self.borderEnlarge = 0
    def update(self):
        self.timer = pygame.time.get_ticks()
        # get coordinates from camera
        self.gameWindow.blit(self.background, [0, 0])
        # Draw
        self.updateCharacters_Objects()
        self.gameOverCheck()    # check for gameover situations

    ## load all characters as attributes for quick access
    def initializeCharactersAndObjects(self):
        self.boss = None
        # Initialize characters
        self.myCharacter = characters("Player",
                           self.gameAssets.allGameImages.allCharacterAnimations["Player"],
                           60, 100, self)
        self.allEntities[self.myCharacter.name] = self.myCharacter
        # Initialize camera
        self.camera = Camera.camera(self, 0, 0)
        self.myCharacter.initCamera(self.camera)
        ## Initialize Objects
        # fill platforms according to map
        for x in range(len(self.map)):
            for y in range(len(self.map)):
                if self.map[x][y] == 1:
                    self.platforms.append(platforms(50, 50,
                                        self.gameAssets.allGameImages.platform1,
                                        (50*x, 50*y), self))


        # Initialize Boss
        self.boss = boss("Hydra", 1000,
                         self.gameAssets.allGameImages.allCharacterAnimations["Hydra"],
                         750, 750, self)

        self.allEntities[self.boss.name] = self.boss
        # Initialize UI
        self.userInterface = UserInterface.userInterface(self)
        self.playerHealthBar = UserInterface.playerHealthBar(0, 10, 300, 40, self.allEntities["Player"], self.gameAssets.allGameImages.playerHealthBar)
        self.blackBorder = pygame.transform.scale(self.gameAssets.allGameImages.blackBorder, [self.wndWidth, 100])
        self.gameAssets.allGameImages.gameOverScreen = pygame.transform.scale(self.gameAssets.allGameImages.gameOverScreen, [self.wndWidth, self.wndHeight])
        self.gameAssets.allGameImages.gameWinScreen = pygame.transform.scale(self.gameAssets.allGameImages.gameWinScreen, [self.wndWidth, self.wndHeight])
    ## Update all objects
    def updateCharacters_Objects(self):
        # Update camera
        self.camera.update()
        # Update boss
        self.boss.update()
        for minion in self.boss.activeMinions:
            minion.update()
        # Update characters
        self.myCharacter.update()
        # Update objects
        for platform in self.platforms:
            platform.update()
        # Update healthbars
        self.userInterface.update()
        self.playerHealthBar.update()
        # update all spell objects, spell objects update their "after effects"
        for spell in self.boss.activeSpells:
            spell.update()
        # Execute whatever state boss is in
        self.boss.bossAI.currentState.Execute()

    # Create a black border
    def createBlackBorder(self):
        self.blackBorder = pygame.transform.scale(self.blackBorder, [self.wndWidth, self.borderEnlarge])
        self.gameWindow.blit(self.blackBorder, [0, 0])
        self.gameWindow.blit(self.blackBorder, [0, self.wndHeight - self.borderEnlarge])
        if self.borderEnlarge < 125:
            self.borderEnlarge += 1


    # take care of game over situations
    def gameOverCheck(self):
        # if player is dead stop
        if self.allEntities["Player"].health == 0:
            self.gameWindow.blit(self.gameAssets.allGameImages.gameOverScreen, [0, 0])
            # if not dead
            if not self.dead:
                # start counting down
                self.gameOverTimer = self.timer
                self.dead = True
                self.gameAssets.allGameSounds.shiftPhaseMusic("sadMusic")
                self.gameOverTimer = self.timer
        else:
            if self.allEntities["Hydra"].health == 0:
                self.gameWindow.blit(self.gameAssets.allGameImages.gameWinScreen, [0, 0])
                # if win boolean is not true yet
                if not self.win:
                    self.gameOverTimer = self.timer
                    self.win = True
                    self.gameAssets.allGameSounds.shiftPhaseMusic("winMusic")
                    self.gameOverTimer = self.timer

        # if died and has been over 5 seconds kill program
        if self.dead and self.timer - self.gameOverTimer > 5000 or self.win and self.timer - self.gameOverTimer > 5000:
            self.gameState.currentInput.runState = False
#
## Class for all characters traits and information
class characters:
    def __init__(self, name, allPlayerAnimations, width,
                 height, game):
        self.name = name
        # Initialize objects we need access to
        self.game = game
        self.gameSounds = game.gameAssets.allGameSounds
        self.gameWindow = self.game.gameWindow
        self.gameState = self.game.gameState
        self.allPlayerAnimations = allPlayerAnimations
        # Initialize window and character dimensions
        self.wndWidth, self.wndHeight = self.gameWindow.get_size()
        self.width = width
        self.height = height
        self.x = 100
        self.y = self.wndHeight - self.wndHeight/2
        # Get player input object
        self.currentInput = self.gameState.currentInput
        #### Character image processing
        # scale images
        for animation in self.allPlayerAnimations:
            for i in range(len(allPlayerAnimations[animation])):
                if animation != "Idle" and i >= 3:
                    allPlayerAnimations[animation][i] = pygame.transform.scale(allPlayerAnimations[animation][i], (self.width + 20, self.height + 10))
                else:
                    allPlayerAnimations[animation][i] = pygame.transform.scale(allPlayerAnimations[animation][i], (self.width, self.height))
        self.image = self.allPlayerAnimations["Idle"][0]  # Default image
        self.animationCounter = 0
        self.tempAnimationCounter = self.animationCounter  # animation counter "mask"
        # Character animation states boolean list
        self.animationStates = {
            "Idle"    : True,
            "Attack1" : False,
            "Move"    : False
        }
        # each player has a controller object
        self.controller = controller(self.currentInput)
        self.physicsManager = physics.physicsBody(self.x, self.y, self.width,
                                                  self.height, True)
        # Initialize character attributes
        self.health = 8     # health is in hearts
        self.attack = 100
        self.speed = 150
        # Timers for delays
        self.timer = pygame.time.get_ticks()
        self.attack1Timer = self.timer

    ## update method for character
    def update(self):
        # Update object timer
        self.timer = pygame.time.get_ticks()
        # Update controls
        self.controller.update()
        # temp save for idle animations
        self.temp = self.animationCounter
        self.manageAttacks()   # Check for attacks
        self.move()     # Check for movements
        self.animate()  # Animate
        # Update all physics (set angle to zero etc)
        self.physicsManager.updatePhysics()
        # ask box2d for x and y coords
        pos = self.physicsManager.getPos()
        self.x = pos[0]
        self.y = pos[1]
        # Draw self when done (self.x is center-> offset by dimension/2)
        drawCoordinates = self.game.camera.relativeToScreen(self.x, self.y, self.width, self.height)
        self.gameWindow.blit(self.image,
                             drawCoordinates)

    ## Move character and move to next animation frame
    def move(self):
        self.animationStates["Move"] = False
        if self.controller.rightPress:  # Apply force in simulation right axis
            self.physicsManager.applyForce((self.speed, 0))
            #self.physicsManager.applyImpulse(100, self.x, self.y)
            self.animationStates["Move"] = True
        if self.controller.leftPress:   # Apply force in simulation left axis
            self.physicsManager.applyForce((-self.speed, 0))
            self.animationStates["Move"] = True
        if self.controller.downPress:   # Apply force in simulation down axis
            self.physicsManager.applyForce((0, self.speed))
            self.animationStates["Move"] = True
        if self.controller.upPress:     # Apply force in simulation up axis
            self.physicsManager.applyForce((0, -self.speed))
            self.animationStates["Move"] = True
        if self.controller.cPress:
            self.camera.tickZoom()

    ## Manage attacks
    def manageAttacks(self):
        if self.controller.attackPress or self.animationStates["Attack1"]:
            self.attack1()

    ## draw character
    def animate(self):
        #### Check which animation state is on then do that animation
        # if moving or standing:
        if self.animationStates["Idle"]:
            self.animationCounter += 1
            self.image = self.allPlayerAnimations["Idle"][self.animationCounter % len(self.allPlayerAnimations["Idle"])]
        if self.animationStates["Attack1"]:
            self.image = self.allPlayerAnimations["Attack1"][self.animationCounter % len(self.allPlayerAnimations["Attack1"])]
        if self.animationStates["Move"] and not self.animationStates["Attack1"]:
            self.animationCounter += 1
        self.physicsManager.body.linearVelocity = (0, 0)

    ##### Player action methods #####
    ## Attack1
    def attack1(self):
        if not self.animationStates["Attack1"]:
            # Set all states to false
            for state in self.animationStates:
                self.animationStates[state] = False
            # Enter attack state
            self.animationStates["Attack1"] = True
            self.animationCounter = 0   # Reset animation counter at beginning
            # Play sound effect
            self.gameSounds.fireSound1.play()
        # Get who is in vicinity: iterate through each and damage?
        if self.timer - self.attack1Timer > 10:
            self.animationCounter += 1
            self.attack1Timer = self.timer
        if self.animationCounter >= len(self.allPlayerAnimations["Attack1"]):
            # check for collision and apply damage
            enemiesInRange = self.aoeCollision(50)
            if enemiesInRange:
                for enemy in enemiesInRange:
                    enemy.takeDamage(50)
            self.animationStates["Attack1"] = False
            self.animationStates["Idle"] = True
            self.animationCounter = 0   # Reset animation counter at end

    ## respond to boss damage
    def takeDamage(self, hearts):
        if hearts >= 0 and self.health > 0:
            if self.health - hearts < 0:
                self.health = 0
            else:
                self.health -= hearts

    ## check if boss in range
    def aoeCollision(self, attackRange):
        enemiesInRange = []
        # Range is from sprite center
        boss = self.game.allEntities["Hydra"]
        if self.x > (boss.x - boss.width // 2) - attackRange and self.x < (boss.x + boss.width//2) + attackRange:
            if self.y > boss.y - boss.height // 2 - attackRange and self.y < boss.y + boss.height // 2 + attackRange:
                enemiesInRange.append(boss)
        for minion in boss.activeMinions:
            if self.x > (minion.x - minion.width // 2) - attackRange and self.x < (minion.x + minion.width//2) + attackRange:
                if self.y > minion.y - minion.height // 2 - attackRange and self.y < minion.y + minion.height // 2 + attackRange:
                    enemiesInRange.append(minion)
        return enemiesInRange

    # change speed
    def changeSpeed(self, speed):
        self.speed = speed

    def initCamera(self, camera):
        self.camera = camera

    def changeCharacter(self, character):
        for category in self.game.gameAssets.allGameImages.allCharacterAnimations[character]:
            for i in range(len(category)):
                self.game.gameAssets.allGameImages.allCharacterAnimations[character][category][i] = pygame.transform.scale(self.game.gameAssets.allGameImages.allCharacterAnimations[character][category][i], (self.width, self.height))
        self.allPlayerAnimations = self.game.gameAssets.allGameImages.allCharacterAnimations[character]



# Controller object decides what character
## should do based on input from input class
class controller:
    def __init__(self, inputKey):
        # input key is inputState from allGameStates
        self.input = inputKey
        # Initialize all variables
        self.leftPress = False
        self.rightPress = False
        self.downPress = False
        self.upPress = False
        self.attackPress = False
        self.cPress = False
        self.spellPress = False
        self.dash = False

    ## take from inputstate
    def update(self):
        keyPress = self.input.getKeyPressed()
        self.cPress = self.input.keyUpC
        if keyPress != []:
            self.upPress = bool(keyPress[pygame.K_w])
            self.leftPress = bool(keyPress[pygame.K_a])
            self.downPress = bool(keyPress[pygame.K_s])
            self.rightPress = bool(keyPress[pygame.K_d])
            self.attackPress = bool(keyPress[pygame.K_SPACE])

#
## Class for platforms you walk on.
class platforms:
    def __init__(self, width, height, image, position, game):
        self.gameWindow = game.gameWindow
        self.camera = game.camera
        self.width = width
        self.height = height
        self.platformImage = pygame.transform.scale(image, (self.width, self.height))
        self.x = position[0]
        self.y = position[1]
        self.physicsManager = physics.physicsBody(self.x, self.y, width, height, False)

    def update(self):
        # Update physics
        self.x, self.y = self.physicsManager.getPos()
        # Draw  self.dimension is center, hence drawing should be offset by dimension/2
        drawCoordinates = self.camera.relativeToScreen(self.x, self.y, self.width, self.height)
        self.gameWindow.blit(self.platformImage, drawCoordinates)


#
## Class for boss
class boss:
    def __init__(self, name, maxHP, animationDictionary, width,
                 height, game):
        # Character, window dimensions and positions
        self.game = game
        self.gameWindow = game.gameWindow
        self.allSpellEffects = self.game.gameAssets.allGameImages.allSpellEffects
        self.wndWidth, self.wndHeight = self.gameWindow.get_size()
        self.camera = game.camera
        self.name = name
        self.maxHP = maxHP   # Max HP
        self.health = maxHP  # boss current health
        self.width = width
        self.height = height
        self.activeSpells = []
        self.activeMinions = []
        # phase one attributes
        self.isImmune = False
        self.isCenteredHorizontally = False
        self.isCenteredVertically = False
        self.phaseOneOver = False
        self.x = 500
        self.y = self.wndHeight - self.wndHeight/2
        # Scale idle animations
        for animation in animationDictionary:
            for i in range(len(animationDictionary[animation])):
                animationDictionary[animation][i] = pygame.transform.scale(animationDictionary[animation][i], [self.width, self.height])
        # scale weather effects
        for i in range(len(self.allSpellEffects["Blizzard"])):
            self.allSpellEffects["Blizzard"][i] = pygame.transform.scale(self.allSpellEffects["Blizzard"][i], [self.wndWidth, self.wndHeight])
        for i in range(len(self.allSpellEffects["Rain"])):
            self.allSpellEffects["Rain"][i] = pygame.transform.scale(self.allSpellEffects["Rain"][i], [self.wndWidth, self.wndHeight])
        # categorize each animation list in animation dictionary
        self.idleAnimations = animationDictionary["Idle"]
        # Default image
        self.image = pygame.transform.scale(self.idleAnimations[0], (self.width, self.height))
        self.animationCounter = 0
        self.fireAnimationCounter = 0
        self.blizzardAnimationCounter = 0
        # AI state machine for controls
        self.initializeStateMachine()  # Creates boss AI attribute
        # initialize timers
        self.timer = pygame.time.get_ticks()
        self.tempTimer = self.timer
        # boss controls his 2 hands
        self.rightHand = bossHands(self.x, self.y, 400, 400, self.game.gameAssets.allGameImages.allCharacterAnimations["Hydra"]["rightHand"], self.game, self, True)
        self.leftHand = bossHands(self.x, self.y, 400, 400, self.game.gameAssets.allGameImages.allCharacterAnimations["Hydra"]["leftHand"], self.game, self, False)

    ## update boss
    def update(self):
        # get total time passed
        self.timer = pygame.time.get_ticks()
        # if time elapsed since last check > 1 second do idle animation
        if self.timer - self.tempTimer > 1000:
            #self.animationCounter += 1   # Increment animation
            self.rightHand.animate()
            self.leftHand.animate()
            self.tempTimer = self.timer  # reset temporary timer
        self.animate()                   # animate and draw
        # consult camera
        drawCoordinates = self.camera.relativeToScreen(self.x, self.y, self.width, self.height)
        self.gameWindow.blit(self.image, drawCoordinates)
        # update both hands
        self.rightHand.update()
        self.leftHand.update()

    ## Animate boss
    def animate(self):
        self.image = self.idleAnimations[self.animationCounter%1]

    ## Initialize AI state machine
    def initializeStateMachine(self):
        # BossAI is the state machine
        self.bossAI = enemyAI.finiteStateMachine()
        self.bossAI.states["IdleState"] = enemyAI.Idle(self)
        self.bossAI.states["AttackState"] = enemyAI.Attack(self)
        self.bossAI.states["PhaseOne"] = enemyAI.phaseOne(self)
        self.bossAI.SetState("IdleState")
        # Kick start state machine
        self.bossAI.Execute()

    ## direction pos-> right negative-> left
    def moveHorizontally(self, direction):
        self.x += direction*3

    ## direction pos -> down negative -> up
    def moveVertically(self, direction):
        self.y += direction*3

    ## Take damage
    def takeDamage(self, amount):
        if amount >= 0 and not self.isImmune:
            self.health -= amount
            self.game.userInterface.bossHPTrail.delayWidth(self.health/self.maxHP)

    #### methods that help state machine script phases
    def becomeImmune(self):
        self.isImmune = True

    def stopImmunity(self):
        self.isImmune = False

    def moveTowardsCenter(self):
        # if difference between boss and center is less than 5, set to center
        if abs(self.x - self.wndWidth//2) < 20:
            self.x = self.wndWidth//2
            self.isCenteredHorizontally = True
        if abs(self.y - self.height//2) < 20:
            self.y = self.wndHeight//2
            self.isCenteredVertically = True
        # if boss is not centered keep moving towards center
        if not self.isCenteredHorizontally:
            if self.x > self.wndWidth // 2:
                self.moveHorizontally(-1)
            if self.x < self.wndWidth // 2:
                self.moveHorizontally(1)
        if not self.isCenteredVertically:
            if self.y > self.wndHeight // 2:
                self.moveVertically(-1)
            if self.y < self.wndHeight // 2:
                self.moveVertically(1)

    def phaseOneBlast(self):
        # create an object of type blast
        self.activeSpells.append(
                                 SpellObjects.expansiveExplosion(
                                                            self,
                                                            self.x, self.y,
                                                            50, 50,
                                                            self.allSpellEffects["PhaseOneBlast"],
                                                            self.game))
        self.game.gameAssets.allGameSounds.startChaozAirflow()
        return

    def castFire(self):
        # blit fire
        fireSpell = self.allSpellEffects["CastingSpell"]
        # play sound
        self.game.gameAssets.allGameSounds.castingFireSound.play()
        # get size of a typical sprite in the spritesheet
        sizeX, sizeY = fireSpell[0].get_size()
        # get draw coordinates from camera and draw
        drawCoordinates = self.camera.relativeToScreen(self.x, self.y, sizeX, sizeY)
        self.gameWindow.blit(fireSpell[self.fireAnimationCounter % len(fireSpell)], drawCoordinates)
        self.fireAnimationCounter += 1      # update animation

    # cast blizzard weather effect
    def castBlizzard(self):
        self.gameWindow.blit(self.allSpellEffects["Blizzard"][self.blizzardAnimationCounter%len(self.allSpellEffects["Blizzard"])], [0, 0])
        # slow down player
        self.game.allEntities["Player"].changeSpeed(3)
        self.blizzardAnimationCounter += 1      # animate
        return

    def spawnMinion(self, name):
        # get player pos, spawn near player
        self.activeMinions.append(Judgement(50, 50, 60, 100, 10, game=self.game, fullAnimations=self.game.gameAssets.allGameImages.allCharacterAnimations["Minion1"]["Idle"]))


#
## class for hands
class bossHands:
    def __init__(self, x, y, width, height, imageList, game, boss, isRight):
        self.boss = boss
        self.camera = self.boss.camera
        self.gameWindow = game.gameWindow
        self.x = x
        self.y = y
        self.isRight = isRight
        self.width = width
        self.height = height
        self.animationList = []
        for image in imageList:
            self.animationList.append(pygame.transform.scale(image,
                                 (self.width, self.height)))
        if isRight:
            for i in range(len(self.animationList)):
                self.animationList[i] = pygame.transform.flip(self.animationList[i], True, False)
        self.animationLen = len(self.animationList)
        self.animationCounter = 0
        self.isCast = False

    def update(self):
        if self.isRight:
            self.x = self.boss.x + 265
        else:
            self.x = self.boss.x - 265
        self.y = self.boss.y - 100
        drawCoordinates = self.camera.relativeToScreen(self.x, self.y, self.width, self.height)
        #drawCoordinates = (self.x, self.y)
        self.gameWindow.blit(self.animationList[self.animationCounter % self.animationLen], drawCoordinates)

    def animate(self):
        if not self.isCast:   # if not casting, keep animating
            self.animationCounter += 1

    def cast(self):
        self.isCast = True
        self.animationCounter = self.animationLen - 1

    def stopCasting(self):
        self.isCast = False


#
## parent class for boss adds / trash mobs
class trashMob:
    def __init__(self, x, y, width, height, maxHP, game):
        # Character, window dimensions and positions
        self.game = game
        self.gameWindow = game.gameWindow
        self.allSpellEffects = self.game.gameAssets.allGameImages.allSpellEffects
        self.wndWidth, self.wndHeight = self.gameWindow.get_size()
        self.camera = game.camera
        self.maxHP = maxHP   # Max HP
        self.health = maxHP  # mob current health
        self.x = x
        self.y = y
        self.width = width
        self.height = height


#
# child judgement inherits from generic trash mob
class Judgement(trashMob):
    def __init__(self, x, y, width, height, maxHP, game, fullAnimations):
        super().__init__(x, y, width, height, maxHP, game)
        self.fullAnimations = fullAnimations
        self.animationLen = len(self.fullAnimations)
        self.animationCounter = 0
        self.timer = pygame.time.get_ticks()
        self.tempTimer = self.timer
        self.mobAI = enemyAI.judgementAI(self)

    def update(self):
        if self.health <= 0:
            self.die()
        drawCoordinates = self.camera.relativeToScreen(self.x, self.y, self.width, self.height)
        self.gameWindow.blit(self.fullAnimations[self.animationCounter % self.animationLen], drawCoordinates)
        self.animate()
        self.mobAI.update()

    def animate(self):
        # animate every second
        self.timer = pygame.time.get_ticks()
        if self.timer - self.tempTimer > 500:
            self.tempTimer = self.timer
            self.animationCounter += 1
        return

    def die(self):
        self.game.allEntities["Hydra"].activeMinions.remove(self)

    def takeDamage(self, damage):
        if damage > 0:
            self.health -= damage