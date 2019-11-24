##############     File to manage AI     ##############
########## AI will be a finite state machine ##########
#### Credit for state machine code skeleton goes to Trevor Payne #####
####      https://www.youtube.com/watch?v=E45v2dD3IQU&t=748s     #####
import pygame
import SpellObjects
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
    def Execute(self):
        # get total time passed
        self.timer = pygame.time.get_ticks()
        # execute every second
        if self.timer - self.tempTimer > 1000:
            print ("Hydra : I AM IDLE, Health: ", self.stateUser.health)
            self.tempTimer = self.timer    # reset temporary timer
        # Update the state machine
        if self.timer - self.attackTimer >  3000:
            self.stateUser.bossAI.SetState("AttackState")
            self.attackTimer = self.timer  # reset timer
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

        # Do attack
        self.Attack1()
        # Change to idle state
        self.stateUser.bossAI.SetState("IdleState")

    def Attack1(self):
        # Create skullbolt object of type bolt
        #self.stateUser.activeSpells.append(SpellObjects.boltSpell(self.stateUser.x,
                    #self.stateUser.y + 50, 150, 150,
                    #self.stateUser.game.gameAssets.allGameImages.allSpellEffects["SkullBolt"],
                    #250, self.stateUser.game.allEntities["Player"]))
        #self.stateUser.activeSpells.append(SpellObjects.boltSpell(self.stateUser.x - 200,
                    #self.stateUser.y + 50, 150, 150,
                    #self.stateUser.game.gameAssets.allGameImages.allSpellEffects["SkullBolt"],
                    #250, self.stateUser.game.allEntities["Player"]))

        print("Hydra : I attacked HAHA")
##============================================================================


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
