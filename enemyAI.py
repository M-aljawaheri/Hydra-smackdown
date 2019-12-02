##############     File to manage AI     ##############
########## AI will be a finite state machine ##########
#### Credit for state machine code skeleton goes to Trevor Payne #####
####      https://www.youtube.com/watch?v=E45v2dD3IQU&t=748s     #####
import pygame
import SpellObjects
import random

##============================================================================
                                                    #<----- All states go Here
# Class for idle boss AI
class Idle:
    def __init__(self, stateUser):
        self.stateUser = stateUser
        # Main timer metric
        self.timer = pygame.time.get_ticks()
        self.tempTimer = self.timer  # Temp timer
        self.turnTimer = self.timer  # turn around timer
        self.attackTimer = self.timer
        self.directionX = 1          # Acts like a boolean -> +1 for right -1 for left
        self.directionY = 1          #                     -> +1 for down  -1 for up
        self.phaseOneOver = False
    def Execute(self):
        # get total time passed
        self.timer = pygame.time.get_ticks()
        # execute every second
        if self.timer - self.tempTimer > 1000:
            pass
        # Update the state machine (transitions)
        if self.timer - self.attackTimer >  3000:
            self.stateUser.bossAI.SetState("AttackState")
            #self.stateUser.camera.setZoom(random.uniform(0.5, 2))
            self.attackTimer = self.timer  # reset timer
        # if exceeded half health, enter phase 2
        if self.stateUser.health < self.stateUser.maxHP / 2 and not self.stateUser.phaseOneOver:
            self.stateUser.bossAI.SetState("PhaseOne")
            self.stateUser.game.gameAssets.allGameSounds.shiftPhaseMusic("PhaseOne")
        self.Move()

    # Take care of idle movement
    def Move(self):
        if self.timer - self.turnTimer > 4000:
            self.directionX *= -1
            self.turnTimer = self.timer    # reset timer
        if self.timer - self.turnTimer > 500:
            self.directionY *= -1
        # Move left and right
        self.stateUser.moveHorizontally(self.directionX)
        self.stateUser.moveVertically(self.directionY)


# Attack player state
class Attack:
    def __init__(self, stateUser):
        self.stateUser = stateUser
    # attack player
    def Execute(self):
        # Determine which attack to do?
        if not self.stateUser.phaseOneOver:
            # Do attack
            self.Attack1()
            self.spawnJudgement()
        else:
            self.Attack2()
        # Change to idle state
        self.stateUser.bossAI.SetState("IdleState")


    def Attack1(self):
        # Create skullbolt object of type bolt
        self.stateUser.activeSpells.append(SpellObjects.boltSpell(self.stateUser.x,
                    self.stateUser.y + 50, 150, 150,
                    self.stateUser.game.gameAssets.allGameImages.allSpellEffects["SkullBolt"],
                    250, self.stateUser.game.allEntities["Player"], "Explosion1"))
        self.stateUser.activeSpells.append(SpellObjects.boltSpell(self.stateUser.x - 200,
                    self.stateUser.y + 50, 150, 150,
                    self.stateUser.game.gameAssets.allGameImages.allSpellEffects["SkullBolt"],
                    250, self.stateUser.game.allEntities["Player"], "Explosion1"))
        pass

    def Attack2(self):
        # Create two fireball object of type bolt
        self.stateUser.activeSpells.append(SpellObjects.boltSpell(self.stateUser.x,
                    self.stateUser.y + 50, 110, 50,
                    self.stateUser.game.gameAssets.allGameImages.allSpellEffects["FireBall"],
                    250, self.stateUser.game.allEntities["Player"], "Firecracker"))
        self.stateUser.activeSpells.append(SpellObjects.boltSpell(self.stateUser.x - 200,
                    self.stateUser.y + 50, 110, 50,
                    self.stateUser.game.gameAssets.allGameImages.allSpellEffects["FireBall"],
                    250, self.stateUser.game.allEntities["Player"], "Firecracker"))

    def spawnJudgement(self):
        # spawn a judgement minion
        self.stateUser.spawnMinion("Judgement")
##============================================================================


#
## Phase 1 state
class phaseOne:
    def __init__(self, stateUser):
        self.stateUser = stateUser
        self.borderOn = True
        self.tempTimer = 0
    def Execute(self):
        # do phase
        if not self.stateUser.isCenteredHorizontally or not self.stateUser.isCenteredVertically:
            self.stateUser.moveTowardsCenter()
            self.startTimer()   # timer will be reinitialized last time when he starts casting
            self.stateUser.becomeImmune()   # Enable immunity
        else:
            self.stateUser.camera.setTarget(self.stateUser.game.allEntities["Hydra"])
            # keep updating state
            self.updateState()
            if self.borderOn:
                self.stateUser.game.createBlackBorder()

        # if out of phase switch back to idle in uodate

    def startTimer(self):
        self.timer = pygame.time.get_ticks()
        self.tempTimer = self.timer


    def updateState(self):
        if self.timer - self.tempTimer > 3000:
            self.stateUser.camera.setTarget(self.stateUser.game.allEntities["Player"])
            self.borderOn = False
        self.timer = pygame.time.get_ticks()
        self.stateUser.castFire()
        self.stateUser.rightHand.cast()
        self.stateUser.leftHand.cast()
        self.stateUser.castBlizzard()
        if self.timer - self.tempTimer > 15000:
            self.stateUser.game.gameAssets.allGameSounds.castingFireSound.stop()
            self.stateUser.leftHand.stopCasting()
            self.stateUser.rightHand.stopCasting()
            # if more than 15 seconds passed, cast spell
            self.stateUser.phaseOneBlast()
            self.stateUser.game.allEntities["Player"].changeSpeed(150)
            self.tempTimer = self.timer
            # go back to idle state
            self.stateUser.phaseOneOver = True
            self.stateUser.bossAI.SetState("IdleState")
            self.stateUser.stopImmunity()   # disable immunity
            self.stateUser.game.allEntities["Player"].changeCharacter("lightningMcQueen")



#
## Our finite state machine
class finiteStateMachine:
    def __init__(self):
        self.states = {}          # All states
        self.currentState = None  # Current state

    ## change state
    def SetState(self, stateName):
        self.currentState = self.states[stateName]

    ## Execute method
    def Execute(self):
        # execute new state
        self.currentState.Execute()
##============================================================================

# rest is for generic AI
class judgementAI:
    def __init__(self, user):
        self.user = user
        self.target = user.game.allEntities["Player"]
        # initialize target and self vector for tracking
        self.targetLocation = pygame.math.Vector2()
        self.targetLocation.xy = self.target.x, self.target.y
        self.posVector = pygame.math.Vector2()
        self.posVector.xy = self.user.x, self.user.y
        self.speed = 0.005

    def update(self):
        self.move()
        self.user.x = self.posVector.x
        self.user.y = self.posVector.y

    def move(self):
        deltaTime = 1/60
        # get direction vector
        directionVector = self.targetLocation - self.posVector
        # calculate distance
        distance = directionVector.length()
        # normalize
        directionVector.normalize()
        if distance > 20:
            self.posVector.xy = self.posVector.x + (directionVector.x*self.speed*deltaTime*0.15*distance), self.posVector.y + (directionVector.y*self.speed*deltaTime*0.15*distance)