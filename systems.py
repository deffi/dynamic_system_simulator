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
        self.acceleration.set(self.force.get() / self.mass)
        self.velocity.set(self.velocity.get() + self.acceleration.get() * dt)
        self.position.set(self.position.get() + self.velocity.get()     * dt)

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
        self.force.set( - self.displacement.get() * self.stiffness)

class SimplePendulum(System):
    def __init__(self, mass, stiffness, friction_coefficient):
        super(SimplePendulum, self).__init__()

        # Parameters
        # Inputs
        # Outputs
        # Subsystems
        self.add_subsystem("mass", SimpleMass(mass))
        self.add_subsystem("spring", SimpleSpring(stiffness))
        
        self.spring.displacement = self.mass.position
        self.mass.force = self.spring.force
        
        # TODO re-enable
        #self.friction_coefficient = friction_coefficient
        
#     def update(self, t, dt):
#         self.mass.update(t, dt)
#         self.spring.displacement = self.mass.position
#         self.spring.update(t, dt)
#         friction = self.friction_coefficient * self.mass.velocity
#         self.mass.force = self.spring.force - friction
