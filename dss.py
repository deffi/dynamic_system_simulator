from matplotlib import pyplot as plt
#from simple_plot.simple_plot import plot as splot

import functions as fn
from system import System
from system import print_system
from systems import Pendulum, TimeFunction
from system_runner import SystemRunner

s = System("system")
pendulum = s.add_subsystem(Pendulum("pendulum", mass=0.5, stiffness=5*1.5, damping=0.1))
gravity = s.add_subsystem(TimeFunction("gravity", lambda t: -0.20*fn.rect((t-5)/5)))

pendulum.mass.position.set(0.1)
pendulum.gravity.connect(gravity.value)

print_system(s)

runner = SystemRunner(s)
runner.add_variable(pendulum.mass.position)
runner.add_variable(gravity.value)
runner.run(16, 0.05)

pos = runner.variables[pendulum.mass.position]
grav = runner.variables[gravity.value]
t = runner.t

plt.plot(t, pos, t, grav)        
#splot(t, x, w=120, h=15, background = " ")
plt.show()
