import Box2D
#########################################################################
######### This class is for calculating game physics using Box2D ########
#########################################################################

# iteration constants for use in game loop
timeStep = 1.0 / 60
vel_iters, pos_iters = 6, 2

# Our box2d simulation world
# will take coordinates in pixels
# Library allows me to create a simulation where I can apply forces
# and library takes care of positions and collisions for me

# Create the simulation world
global world
world = Box2D.b2World(gravity=(0, 10), doSleep=True)


#
## Physics manager object
class physicsBody:
    global world
    #### Library mechanism ####
    # Create a body that acts as a sort of center of mass
    # Create a shape around that body that represents geometry for collisions
    # Create a fixture that joins body and shape, takes care of properties e.g density

    def __init__(self, xpos, ypos, dimensionX, dimensionY, isDynamic):
        # Creating the body definition
        self.bodyDef = Box2D.b2BodyDef()
        if isDynamic:
            self.bodyDef.type = Box2D.b2_dynamicBody
        else:
            self.bodyDef.type = Box2D.b2_staticBody
            # put object to "Sleep" to spare CPU
            self.bodyDef.awake = False
        self.bodyDef.position = (xpos, ypos)
        # platform body in world
        self.body = world.CreateBody(self.bodyDef)
        self.body.mass = 0.001
        # platform box shape
        self.objectBox = Box2D.b2PolygonShape(box=(dimensionX/2, dimensionY/2))
        # fixture definition
        if isDynamic:
            self.objectBoxFixture = Box2D.b2FixtureDef(shape=self.objectBox)
        else:
            self.objectBoxFixture = Box2D.b2FixtureDef(shape=self.objectBox, density=1, friction=0.3)
        self.body.CreateFixture(self.objectBoxFixture)

        # the boundaries
        # The boundaries
        ground = world.CreateBody(position=(400, 0))
        ground.CreateEdgeChain(
            [(-1200, -1200),
             (-1200, 1200),
             (2000, 2000),
             (2000, -1200),
             (-1200, -1200)]
        )

        world.CreateFrictionJoint(bodyA=ground, bodyB=self.body)

        # transform point
        #self.createTransformPoint()

    #def createTransformPoint(self):
        #self.transform = Box2D.b2Transform()
        #self.transform.SetIdentity()
        #self.hit = self.objectBox.TestPoint(self.transform, (5, 2))

    def getPos(self):
        pos = self.body.position
        return pos

    def applyForce(self, force):
        # Get center of mass in simulation coordinates
        vec2Pos = self.body.worldCenter
        vec2Pos.xy = vec2Pos.x, vec2Pos.y
        # Apply force
        self.body.ApplyForce(force=force, point=vec2Pos, wake=True)

    def applyImpulse(self, impulse, x, y):
        # Get center of mass in simulation coordinates
        vec2Pos = self.body.worldCenter
        self.body.ApplyLinearImpulse(Box2D.b2Vec2(100, 0), vec2Pos, True)

    def updatePhysics(self):
        # Set angular damping to zero to avoid spinning
        self.body.angularDamping = 0
        # Reset angle
        self.body.angle = 0.0
        # Apply downwards force
        #self.applyForce((0, 350))
