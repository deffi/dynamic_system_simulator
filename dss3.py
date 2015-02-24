#from matplotlib import pyplot as plt
from simple_plot.simple_plot import plot as splot

from system3 import System
 
# import library.functions as fn
# from system import System
# from system import print_system
# from library.systems import Pendulum, TimeFunction
# from system_runner import SystemRunner
# 
#

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

        #force.connect((-damping) * velocity)
        
    def update(self, var, t, dt):
        var.force = - var.velocity * self.damping

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



        
        
# 
# s = PendulumWithGravity("system")
# print_system(s)
# 
# runner = SystemRunner(s)
# runner.add_variable(s.pendulum.mass.position)
# runner.add_variable(s.gravity.value)
# runner.run(16, 0.05)
# 
# pos = runner.variables[s.pendulum.mass.position]
# grav = runner.variables[s.gravity.value]
# t = runner.t
# 
# plt.plot(t, pos, t, grav)        
# #splot(t, x, w=120, h=15, background = " ")
# plt.show()
