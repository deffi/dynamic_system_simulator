import numpy as np
from matplotlib import pyplot as plt

from system import print_system
from systems import Pendulum

#from simple_plot.simple_plot import plot

# t = np.arange(0, 10, 0.1)
# x = np.zeros(np.size(t))

pendulum = Pendulum("pendulum", mass=0.5, stiffness=1.5, damping=0.1, gravity = 0.5)

# Or pendulum.spring.displacement
pendulum.mass.position=1

print_system(pendulum)

t = [t*0.1 for t in range(120)]
x = [0] * len(t)
 
for i in range(len(t)):
    x[i] = pendulum.mass.position
 
    dt = t[i]-t[i-1] if i>0 else None
    if i>0:
        pendulum.update(t[i], dt)

#plot(t, x, w=120, h=15, background = " ")


plt.plot(t, x)        
plt.show()
