# import math
# import numpy as np
# from matplotlib import pyplot as plt

from system import *

if __name__ == '__main__':
#     #wheel_system=ChainSystem([RateLimiter(1, 1), Motor(1, 1, 0.1), Integrator()])
#     wheel_system=ChainSystem([Motor(1, 1, 0.1), Integrator()])
#     system=ControlledSystem(wheel_system, PController(1))
#     #system=ControlledSystem(wheel_system, PIDController(1, 0.1, 0.5))
# 
#     time = 20
#     dt = 1/50
# 
#     def u(t):
#         if t>=1:
#             return 1
#         else:
#             return 0
# 
#     u=lambda t: 1
# 
#     T=np.arange(0, time+dt, dt)
#     
#     Y=np.zeros(np.size(T))
#      
#     Y[0]=system.output()
#     previous_t=T[0]
#     for i, t in enumerate(T[1:]):
#         system.update(dt, u(t))
#         Y[i+1]=system.output()
# 
#     plt.plot(T, Y, '-')
#     plt.grid()
#     plt.show()

    # Simulate a spring pendulum
    mass = 1
    stiffness = 1
    
    spring = Gain(input="position", output="force", gain=-stiffness)
    mass1 = Gain(input="force", output="acceleration", gain=1/mass)
    mass2 = Integrator(input="acceleration", output="velocity")
    mass3 = Integrator(input="velocity", output="position")
    


'''

# Open questions:
#   - parameters
#   - initial values
#   - subsystems (e. g. spring, vehicle with 4 wheels)
#   - visualization (also internal values: pwm values in a motor controller
#     system, integral error in a PID controller)

'''
