import math
import numpy as np
from matplotlib import pyplot as plt

'''

# Open questions:
#   - parameters
#   - setting initial values from outside
#   - subsystems (e. g. spring, vehicle with 4 wheels)
#   - visualization (also internal values: pwm values in a motor controller
#     system, integral error in a PID controller)

'''

from system import System

class Spring(System):
    def __init__(self):
        self.displacement = 0
        
    def setup(self):
        pass
        #self.input("displacement", 0)
        #self.output("force")
        #self.parameter("stiffness")
    
    def initialize(self):
        pass
        
    def update(self, t, dt):
        self.force = - self.displacement * self.stiffness

class Mass(System):
    def setup(self):
        pass
        #self.input("force")
        #self.output("position")
        #self.parameter("mass")
        #self.internal("acceleration")
        #self.internal("velocity")

    def __init__(self):        
        self.position = 0
        self.velocity = 0
        
    def update(self, t, dt):
        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration * (dt or 0)
        self.position += self.velocity * (dt or 0)

class Pendulum(System):
    def __init__(self):
        self.spring = Spring()
        self.mass   = Mass()
        
    def setup(self):
        pass
        #self.parameter("stiffness")
        #self.parameter("mass")
        
    def update(self, t, dt):
        self.spring.displacement = self.mass.position
        self.spring.update(t, dt)
        
        self.mass.force = self.spring.force
        self.mass.update(t, dt)
        

# T = 2 π sqrt(m/D)

pendulum = Pendulum()
pendulum.spring.stiffness = 1.5
pendulum.mass.mass = 0.5

# It must be irrelevant which one we assign to, because it's the same variable
pendulum.mass.position = 1
#pendulum.spring.displacement = 1

t = np.arange(0, 10, 0.1)
x = np.zeros(np.size(t))

for i in range(len(t)):
    x[i] = pendulum.mass.position

    dt = t[i]-t[i-1] if i>0 else None
    pendulum.update(t, dt)


#pendulum.run(10, 0.01)

#plt.plot(pendulum.time(), pendulum.position.log())
plt.plot(t, x)        
plt.show()
