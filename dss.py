import numpy as np
from matplotlib import pyplot as plt

from system import System
from system import print_system
from systems import Pendulum, TimeFunction

#from simple_plot.simple_plot import plot

# t = np.arange(0, 10, 0.1)
# x = np.zeros(np.size(t))

step = lambda t: 1 if t>0 else 0
rect = lambda t: 1 if t>0 and t<1 else 0


s = System("system")
pendulum = s.add_subsystem(Pendulum("pendulum", mass=0.5, stiffness=5*1.5, damping=0.1))
gravity = s.add_subsystem(TimeFunction("gravity", lambda t: -5*rect((t-5)/5)))

pendulum.mass.position = 1
pendulum.variables.gravity.connect(gravity.variables.value)

print_system(s)


t = [t*0.1 for t in range(120)]
x = [0] * len(t)
 
for i in range(len(t)):
    x[i] = pendulum.mass.position
 
    dt = t[i]-t[i-1] if i>0 else None
    if i>0:
        s.update(t[i], dt)

#plot(t, x, w=120, h=15, background = " ")


plt.plot(t, x)        
plt.show()
