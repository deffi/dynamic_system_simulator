from system import System
 
class Mass(System):
    def __init__(self, name, mass, position = 0, velocity = 0):
        super(Mass, self).__init__(name)

        # Parameters
        self.mass = mass
        # Inputs
        self.add_input("force", 0)
        # Outputs
        self.add_output("velocity", 0)
        self.add_output("position", 0)
        self.add_output("acceleration", 0)
        
    def update(self, t, dt):
        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration * dt
        self.position += self.velocity     * dt

class Spring(System):
    def __init__(self, name, stiffness = 1):
        super(Spring, self).__init__(name)

        # Parameters
        self.stiffness = stiffness
        # Inputs
        self.add_input("displacement", 0)
        # Outputs
        self.add_output("force", 0)
    
    def update(self, t, dt):
        self.force = - self.displacement * self.stiffness

class Damper(System):
    def __init__(self, name, damping = 1):
        super(Damper, self).__init__(name)
        
        self.damping = damping
        
        self.add_input("velocity", 0)
        self.add_output("force", 0)
        
    def update(self, t, dt):
        self.force = - self.velocity * self.damping

class Pendulum(System):
    def __init__(self, name, mass, stiffness, damping, gravity):
        super(Pendulum, self).__init__(name)

        self.gravity = gravity

        mass   = self.add_subsystem(Mass  ("mass"  , mass))
        spring = self.add_subsystem(Spring("spring", stiffness))
        damper = self.add_subsystem(Damper("damper", damping))
        
        spring.variables.displacement.connect(mass.variables.position)
        damper.variables.velocity.connect(mass.variables.velocity)
        # Without damper (direct connection)
        #mass.variables.force.connect(spring.variables.force)
        # With damper (callable)
        mass.variables.force.connect(lambda: spring.force + damper.force + self.gravity)
        
        # Good
        #mass.force.connect(spring.force + damper.force)
        #mass["force"].connect(spring["force"] + damper["force"])
        #mass["force"] = spring["force"] + damper["force"]        

