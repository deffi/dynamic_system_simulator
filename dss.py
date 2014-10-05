#import numpy as np
# from matplotlib import pyplot as plt

from systems import SimplePendulum

from simple_plot.simple_plot import plot

# pendulum = Pendulum()
# 
# pendulum.spring.stiffness.set(1.5)
# pendulum.mass.mass.set(0.5)
# # It should be irrelevant which one we assign to, because it's the same variable
# pendulum.mass.position.set(1)
# #pendulum.spring.displacement = 1

# t = np.arange(0, 10, 0.1)
# x = np.zeros(np.size(t))

pendulum = SimplePendulum(mass=0.5, stiffness=1.5, friction_coefficient=0.1, initial_position=1)

t = [t*0.1 for t in range(150)]
x = [0] * len(t)
 
for i in range(len(t)):
    x[i] = pendulum.mass.position
 
    dt = t[i]-t[i-1] if i>0 else None
    if i>0:
        pendulum.update(t[i], dt)

plot(t, x, w=120, h=15, background = " ")


# plt.plot(t, x)        
# plt.show()
