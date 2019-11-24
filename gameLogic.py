import pygame
import physics
import enemyAI
import UserInterface

# Main game object, will be pointed at by currentState
## update() method continuously updates the game
class mainGame:
    def __init__(self, gameAssets, gameState, gameWindow):
        # All classes access resources e.g assets and window/states from here
        self.gameWindow = gameWindow
        self.gameAssets = gameAssets
        self.gameState = gameState
        self.platforms = []
        self.allEntities = {}
        # load all characters and inanimate objects as attributes
        self.initializeCharactersAndObjects()
        self.wndWidth, self.wndHeight = gameWindow.get_size()
        self.gameAssets.allGameImages.gameBackground = pygame.transform.scale(self.gameAssets.allGameImages.gameBackground,
                                                                              (self.wndWidth, self.wndHeight))

    def update(self):
        # Get background and draw
        background = self.gameAssets.allGameImages.gameBackground
        self.gameWindow.blit(background, [0, 0])
        self.updateCharacters_Objects()

    ## load all characters as attributes for quick access
    def initializeCharactersAndObjects(self):
        # Initialize characters
        self.myCharacter = characters("Player",
                           self.gameAssets.allGameImages.allCharacterAnimations["Player"],
                           60, 100, self)
        self.allEntities[self.myCharacter.name] = self.myCharacter

        # Initialize Objects
        for i in range(30):
            self.platforms.append(platforms(50, 50,
                                  self.gameAssets.allGameImages.platform1,
                                  (50*i, 500), self))

        # Initialize Boss
        self.boss = boss("Hydra", 1000,
                         self.gameAssets.allGameImages.allCharacterAnimations["Hydra"],
                         750, 750, self)
        self.allEntities[self.boss.name] = self.boss
        # Initialize UI
        self.userInterface = UserInterface.userInterface(self)


    ## Update all objects
    def updateCharacters_Objects(self):
        # Update boss
        self.boss.update()
        # Update characters
        self.myCharacter.update()
        # Update objects
        for platform in self.platforms:
            platform.update()
        # Update healthbar
        self.userInterface.update()
        # update all spell objects, spell objects update their "after effects"
        for spell in self.boss.activeSpells:
            spell.update()


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
        self.x = 0
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
        self.health = 500
        self.attack = 100
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
        self.gameWindow.blit(self.image,
                             [self.x - self.width/2, self.y - self.height/2])

    ## Move character and move to next animation frame
    def move(self):
        self.animationStates["Move"] = False
        if self.controller.rightPress:  # Apply force in simulation right axis
            self.physicsManager.applyForce((100, 0))
            #self.physicsManager.applyImpulse((100, 0))
            self.animationStates["Move"] = True
        if self.controller.leftPress:   # Apply force in simulation left axis
            self.physicsManager.applyForce((-150, 0))
            self.animationStates["Move"] = True
        if self.controller.downPress:   # Apply force in simulation down axis
            self.physicsManager.applyForce((0, 150))
            self.animationStates["Move"] = True
        if self.controller.upPress:     # Apply force in simulation up axis
            self.physicsManager.applyForce((0, -150))
            self.animationStates["Move"] = True

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
        #if self.animationCounter == self.temp:
        #self.temp = self.animationCounter
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
        #print("Me : I am ATTACKING")
        if self.timer - self.attack1Timer > 10:
            self.animationCounter += 1
            self.attack1Timer = self.timer
        if self.animationCounter >= len(self.allPlayerAnimations["Attack1"]):
            self.game.allEntities["Hydra"].takeDamage(5)
            self.animationStates["Attack1"] = False
            self.animationStates["Idle"] = True
            self.animationCounter = 0   # Reset animation counter at end

    ## respond to boss damage
    def takeDamage(self, damage):
        if damage >= 0:
            self.health -= damage

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
        self.spellPress = False
        self.dash = False

    ## take from inputstate
    def update(self):
        keyPress = self.input.getKeyPressed()
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
        self.gameWindow.blit(self.platformImage, [self.x - self.width/2, self.y - self.height /2])


#
## Class for boss
class boss:
    def __init__(self, name, maxHP, animationDictionary, width,
                 height, game):
        # Character, window dimensions and positions
        self.game = game
        self.gameWindow = game.gameWindow
        self.wndWidth, self.wndHeight = self.gameWindow.get_size()
        self.name = name
        self.maxHP = maxHP   # Max HP
        self.health = maxHP  # boss current health
        self.width = width
        self.height = height
        self.activeSpells = []
        self.x = 500
        self.y = self.wndHeight - self.wndHeight/2
        # Scale idle animations
        for animation in animationDictionary:
            for i in range(len(animationDictionary[animation])):
                animationDictionary[animation][i] = pygame.transform.scale(animationDictionary[animation][i], [self.width, self.height])
        # categorize each animation list in animation dictionary
        self.idleAnimations = animationDictionary["Idle"]
        # Default image
        self.image = pygame.transform.scale(self.idleAnimations[2], (self.width, self.height))
        self.animationCounter = 0
        # AI state machine for controls
        self.initializeStateMachine()  # Creates boss AI attribute
        # initialize timers
        self.timer = pygame.time.get_ticks()
        self.tempTimer = self.timer

    ## update boss
    def update(self):
        # get total time passed
        self.timer = pygame.time.get_ticks()
        # if time elapsed since last check > 1 second do idle animation
        if self.timer - self.tempTimer > 1000:
            self.animationCounter += 1   # Increment animation
            self.tempTimer = self.timer  # reset temporary timer
        # Execute whatever state boss is in
        self.bossAI.currentState.Execute()
        self.animate()                   # animate and draw
        self.gameWindow.blit(self.image, [self.x - self.width/2, self.y - self.height / 2])

    ## Animate boss
    def animate(self):
        self.image = self.idleAnimations[self.animationCounter%3]

    ## Initialize AI state machine
    def initializeStateMachine(self):
        # BossAI is the state machine
        self.bossAI = enemyAI.finiteStateMachine()
        self.bossAI.states["IdleState"] = enemyAI.Idle(self)
        self.bossAI.states["AttackState"] = enemyAI.Attack(self)
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
        if amount >= 0:
            self.health -= amount
