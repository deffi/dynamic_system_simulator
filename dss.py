# import math
# import numpy as np
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
    def setup(self):
        self.input("displacement")
        self.output("force")
        self.parameter("stiffness")
    
    def initialize(self):
        pass
        
    def update(self, t, dt):
        self.force = - self.position * self.stiffness

class Mass(System):
    def setup(self):
        self.input("force")
        self.output("position")
        self.parameter("mass")
        self.internal("acceleration")
        self.internal("velocity")
        
    def initialize(self):
        self.velocity = 0
        
    def step(self, dt, input_):
        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

class Pendulum(System):
    def setup(self):
        self.parameter("stiffness")
        self.parameter("mass")
        
        spring = Spring(self, "spring", displacement="position", force="force", stiffness = self.stiffness)
        mass   = Mass  (self, "mass"  , force="force", position="position", mass = self.mass)

pendulum = Pendulum()
pendulum.mass = 1
pendulum.stiffness = 1
pendulum.position = 1
pendulum.run(10, 0.01)

plt.plot(pendulum.time(), pendulum.position.log())        
plt.show()
