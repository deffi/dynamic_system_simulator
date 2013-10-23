import math
import numpy as np
from matplotlib import pyplot as plt

'''

# Open questions:
#   - parameters
#   - setting initial values from outside (like parameters, or as parameters)
#   - subsystems (e. g. vehicle with 4 wheels)
#   - visualization (also internal values: pwm values in a motor controller
#     system, integral error in a PID controller)

'''

from systems import Pendulum

pendulum = Pendulum()
pendulum.spring.stiffness = 1.5
pendulum.mass.mass = 0.5
# It should be irrelevant which one we assign to, because it's the same variable
pendulum.mass.position = 1
#pendulum.spring.displacement = 1

t = np.arange(0, 10, 0.1)
x = np.zeros(np.size(t))

for i in range(len(t)):
    x[i] = pendulum.mass.position

    dt = t[i]-t[i-1] if i>0 else None
    pendulum.update(t[i], dt)

plt.plot(t, x)        
plt.show()
