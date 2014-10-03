from system import System
 
# def getx(self):
#     print("getting it")
#     return self._x
# 
# def setx(self, value):
#     print("setting it")
#     self._x = value
#     
# def delx(self):
#     print("deleting it")
#     del self._x
# 
# MyClass.x = property(getx, setx, delx, "I'm the 'x' property.")

# def variable_property(variable):
#     def getter(self, ):
# 
# class 

class SimpleMass(System):
    def __init__(self, mass, position = 0, velocity = 0):
        # Parameters
        self.mass = mass
        # Inputs
        self.force = 0
        # Outputs
        self.velocity = velocity
        self.position = position
        self.acceleration = 0
        
    def update(self, t, dt):
        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration * dt
        self.position += self.velocity     * dt

class SimpleSpring(System):
    def __init__(self, stiffness = 1):
        # Parameters
        self.stiffness = stiffness
        # Inputs
        self.displacement = None
        # Outputs
        self. force = None
    
    def update(self, t, dt):
        self.force = - self.displacement * self.stiffness

class SimplePendulum(System):
    def __init__(self, mass, stiffness, friction_coefficient, initial_position):
        # Parameters
        # Inputs
        # Outputs
        # Subsystems
        # TODO next exercise: add friction
        self.mass = SimpleMass(mass, position = initial_position)
        self.spring = SimpleSpring(stiffness)
        self.friction_coefficient = friction_coefficient
        
    def update(self, t, dt):
        self.mass.update(t, dt)
        self.spring.displacement = self.mass.position
        self.spring.update(t, dt)
        friction = self.friction_coefficient * self.mass.velocity
        self.mass.force = self.spring.force - friction
        
    

class Mass(System):
    def setup(self):
        self.input("force")
        self.output("position")
        
        self.parameter("mass", 1)
        
        self.internal("acceleration", 0)
        self.internal("velocity"    , 0)

    def update(self, t, dt):
        # FIXME: sometimes, force seems to be None.
        self.acceleration.set(self.force.get() / self.mass.get())
        self.velocity.set(self.velocity.get() + self.acceleration.get() * (dt or 0))
        self.position.set(self.position.get() + self.velocity    .get() * (dt or 0))

        #self.position.set(self.position.get() + self.velocity    .get() * (dt or 0))
        #self.position += self.velocity * (dt or 0)
        #position.set(position.get() + velocity.get() * (dt or 0))
        #position += velocity * (dt or 0)

class Spring(System):
    def setup(self):
        self.input("displacement")
        self.output("force")
        self.parameter("stiffness", 1)
        
    def update(self, t, dt):
        # This is what we want
        #self.force = - self.displacement * self.stiffness
        self.force.set(- self.displacement.get() * self.stiffness.get())

        

class Pendulum(System):
    def setup(self):
        self.subsystem("mass"  , Mass  ())
        self.subsystem("spring", Spring())
        
        self.connect(self.mass.position, self.spring.displacement)
        self.connect(self.spring.force, self.mass.force)
