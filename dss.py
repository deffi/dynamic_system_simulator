#import math

import numpy as np
from matplotlib import pyplot as plt

from system import System
from system import print_system
from systems import Pendulum, TimeFunction

#from simple_plot.simple_plot import plot as splot

step = lambda t: 1 if t>0 else 0
rect = lambda t: 1 if t>0 and t<1 else 0

s = System("system")
pendulum = s.add_subsystem(Pendulum("pendulum", mass=0.5, stiffness=5*1.5, damping=0.1))
gravity = s.add_subsystem(TimeFunction("gravity", lambda t: -1*rect((t-5)/5)))

#pendulum.mass.position.set(0.1)
pendulum.mass.variables_wrapper.position=0.1
pendulum.gravity.connect(gravity.value)

print_system(s)

time = 16
step = 0.05

t = np.arange(0, time, step)
x = np.zeros(np.size(t))
y = np.zeros(np.size(t))

# t = [t*step for t in range(math.floor(time/step))]
# x = [0] * len(t)
 
 
for i in range(len(t)):
    #print(pendulum.spring.displacement.get(), pendulum.spring.force.get())
    x[i] = float(pendulum.mass.position)
    y[i] = float(gravity.value)
 
    dt = t[i]-t[i-1] if i>0 else None
    if i>0:
        s.update(s.variables_wrapper, t[i], dt)

#splot(t, x, w=120, h=15, background = " ")


plt.plot(t, x, t, y)        
plt.show()
