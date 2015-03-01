#from matplotlib import pyplot as plt
from simple_plot.simple_plot import plot as splot

from system3 import System, CompositeSystem
from system_runner_3 import SystemRunner
from variable3 import ArithmeticVariable
 
# from system import print_system

class Mass(System):
    def __init__(self, name, mass, position = 0, velocity = 0):
        super(Mass, self).__init__(name)

        # Parameters
        self.mass = mass
        # Inputs
        self.add_input("force")
        # Outputs
        self.add_output("velocity", 0)
        self.add_output("position", 0)
        self.add_output("acceleration", 0)
        
    def update(self, clock):
        var = self.variables_wrapper
        var.acceleration = var.force / self.mass
        var.velocity += var.acceleration * clock.dt
        var.position += var.velocity     * clock.dt

class Spring(System):
    def __init__(self, name, stiffness = 1):
        super(Spring, self).__init__(name)

        # Parameters
        self.stiffness = stiffness
        # Inputs
        self.add_input("displacement")
        # Outputs
        self.add_output("force", 0)
    
    def update(self, clock):
        var = self.variables_wrapper
        var.force = - var.displacement * self.stiffness

class Damper(System):
    def __init__(self, name, damping = 1):
        super(Damper, self).__init__(name)
        
        self.damping = damping

        self.add_input("velocity")
        self.add_output("force", 0)

    def update(self, clock):
        var = self.variables_wrapper
        var.force = - var.velocity * self.damping

class Pendulum(CompositeSystem):
    def __init__(self, name, mass, stiffness, damping):
        super(Pendulum, self).__init__(name)

        self.mass   = self.add_subsystem(Mass  ("mass"  , mass     ))
        self.spring = self.add_subsystem(Spring("spring", stiffness))
        self.damper = self.add_subsystem(Damper("damper", damping  ))
        
        self.spring.displacement.connect(self.mass.position)
        self.damper.velocity.connect(self.mass.velocity)
        #mass.force.connect(spring.force + damper.force)
        self.mass.force.connect(ArithmeticVariable("sum", (self.spring.force, self.damper.force), lambda a, b: a+b))



pendulum = Pendulum("pendulum", mass=0.5, stiffness=5*1.5, damping=0.1)
# print_system(s)
#

pendulum.mass.position.set_value(0.1)
 
runner = SystemRunner(pendulum)
runner.add_variable(pendulum.mass.position)
#runner.add_variable(pendulum.gravity.value)
runner.run(16, 0.05)
 
pos = runner.variables[pendulum.mass.position]
t = runner.t
 
splot(t, pos, w=120, h=15, background = " ")
#plt.plot(t, pos, t, grav)        
#plt.show()
