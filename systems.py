from system import System

class Spring(System):
    def setup(self):
        self.input("displacement")
        self.output("force")
        self.parameter("stiffness", 1)
        
    def update(self, t, dt):
        # This is what we want
        #self.force = - self.displacement * self.stiffness
        self.force.set(- self.displacement.get() * self.stiffness.get())

class Mass(System):
    def setup(self):
        self.input("force")
        self.output("position")
        
        self.parameter("mass", 1)
        
        self.internal("acceleration", 0)
        self.internal("velocity"    , 0)

    def update(self, t, dt):
        self.acceleration.set(self.force.get() / self.mass.get())
        self.velocity.set(self.velocity.get() + self.acceleration.get() * (dt or 0))
        self.position.set(self.position.get() + self.velocity    .get() * (dt or 0))

        #self.position.set(self.position.get() + self.velocity    .get() * (dt or 0))
        #self.position += self.velocity * (dt or 0)
        #position.set(position.get() + velocity.get() * (dt or 0))
        #position += velocity * (dt or 0)
        

class Pendulum(System):
    def setup(self):
        self.subsystem("mass"  , Mass  ())
        self.subsystem("spring", Spring())
        
        self.connect(self.mass.position, self.spring.displacement)
        self.connect(self.spring.force, self.mass.force)
