from matplotlib import pyplot as plt
#from simple_plot.simple_plot import plot as splot

import functions as fn
from system import System
from system import print_system
from systems import Pendulum, TimeFunction
from system_runner import SystemRunner

class MySystem(System):
    def __init__(self, name):
        super(MySystem, self).__init__(name)

        pendulum = self.add_subsystem(Pendulum("pendulum", mass=0.5, stiffness=5*1.5, damping=0.1))
        gravity = self.add_subsystem(TimeFunction("gravity", lambda t: -0.20*fn.rect((t-5)/5)))

        pendulum.mass.position.set(0.1)
        pendulum.gravity.connect(gravity.value)

s = MySystem("system")
print_system(s)

runner = SystemRunner(s)
runner.add_variable(s.pendulum.mass.position)
runner.add_variable(s.gravity.value)
runner.run(16, 0.05)

pos = runner.variables[s.pendulum.mass.position]
grav = runner.variables[s.gravity.value]
t = runner.t

plt.plot(t, pos, t, grav)        
#splot(t, x, w=120, h=15, background = " ")
plt.show()
