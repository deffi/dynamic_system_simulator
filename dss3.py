#from matplotlib import pyplot as plt
from simple_plot.simple_plot import plot as splot

from system3 import System, CompositeSystem
from system_runner_3 import SystemRunner
 
# from system import print_system

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
        
    def update(self, var, clock):
        var.acceleration = var.force / self.mass
        var.velocity += var.acceleration * clock.dt
        var.position += var.velocity     * clock.dt

class Spring(System):
    def __init__(self, name, stiffness = 1):
        super(Spring, self).__init__(name)

        # Parameters
        self.stiffness = stiffness
        # Inputs
        self.add_input("displacement", 0)
        # Outputs
        self.add_output("force", 0)
    
    def update(self, var, clock):
        var.force = - var.displacement * self.stiffness

class Damper(System):
    def __init__(self, name, damping = 1):
        super(Damper, self).__init__(name)
        
        self.damping = damping

        self.add_input("velocity", 0)
        self.add_output("force", 0)

    def update(self, var, clock):
        var.force = - var.velocity * self.damping

class Pendulum(CompositeSystem):
    def __init__(self, name, mass, stiffness, damping):
        super(Pendulum, self).__init__(name)

        mass   = self.add_subsystem(Mass  ("mass"  , mass     ))
        spring = self.add_subsystem(Spring("spring", stiffness))
        damper = self.add_subsystem(Damper("damper", damping  ))
        
        spring.displacement.connect(mass.position)
        damper.velocity.connect(mass.velocity)
        mass.force.connect(spring.force + damper.force)



pendulum = Pendulum("pendulum")
# print_system(s)
# 
runner = SystemRunner(pendulum)
runner.add_variable(pendulum.pendulum.mass.position)
runner.add_variable(pendulum.gravity.value)
runner.run(16, 0.05)
 
pos = runner.variables[pendulum.mass.position]
t = runner.t
 
#plt.plot(t, pos, t, grav)        
splot(t, pos, w=120, h=15, background = " ")
#plt.show()
