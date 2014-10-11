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
        
    def update(self, var, t, dt):
        var.acceleration = var.force / self.mass
        var.velocity += var.acceleration * dt
        var.position += var.velocity     * dt

class Spring(System):
    def __init__(self, name, stiffness = 1):
        super(Spring, self).__init__(name)

        # Parameters
        self.stiffness = stiffness
        # Inputs
        self.add_input("displacement", 0)
        # Outputs
        self.add_output("force", 0)
    
    def update(self, var, t, dt):
        var.force = - var.displacement * self.stiffness

class Damper(System):
    def __init__(self, name, damping = 1):
        super(Damper, self).__init__(name)
        
        # TODO must be a variable so it can be changed
        self.damping = damping

        velocity = self.add_input("velocity", 0)
        force    = self.add_output("force", 0)

        force.connect((-damping) * velocity)
        
    #def update(self, var, t, dt):
    #    var.force = - var.velocity * self.damping

class Pendulum(System):
    def __init__(self, name, mass, stiffness, damping):
        super(Pendulum, self).__init__(name)

        gravity = self.add_input("gravity", 0)

        mass   = self.add_subsystem(Mass  ("mass"  , mass     ))
        spring = self.add_subsystem(Spring("spring", stiffness))
        damper = self.add_subsystem(Damper("damper", damping  ))
        
        spring.displacement.connect(mass.position)
        damper.velocity.connect(mass.velocity)
        mass.force.connect(spring.force + damper.force + gravity)


class TimeFunction(System):
    def __init__(self, name, function):
        super(TimeFunction, self).__init__(name)
        self._function = function
        self.add_output("value", function(0))
        
    def update(self, var, t, dt):
        var.value = self._function(t)
        