from system import System
 
class SimpleMass(System):
    def __init__(self, mass, position = 0, velocity = 0):
        super(SimpleMass, self).__init__()

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

class SimpleSpring(System):
    def __init__(self, stiffness = 1):
        super(SimpleSpring, self).__init__()

        # Parameters
        self.stiffness = stiffness
        # Inputs
        self.add_input("displacement", 0)
        # Outputs
        self.add_output("force", 0)
    
    def update(self, t, dt):
        self.force = - self.displacement * self.stiffness

class SimplePendulum(System):
    def __init__(self, mass, stiffness, friction_coefficient):
        super(SimplePendulum, self).__init__()

        # Parameters
        # Inputs
        # Outputs
        # Subsystems
        self.add_subsystem("mass", SimpleMass(mass))
        self.add_subsystem("spring", SimpleSpring(stiffness))
        
        self.spring.variables.displacement = self.mass.variables.position
        self.mass.variables.force = self.spring.variables.force
        
        # TODO re-enable:
        #self.friction_coefficient = friction_coefficient
        # mass.force = spring.force - friction_coefficient * mass.velocity
