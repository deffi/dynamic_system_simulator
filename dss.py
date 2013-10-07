import math
import numpy as np
from matplotlib import pyplot as plt



def limit(value, minimum=None, maximum=None, absolute=False):
    if absolute:
        return math.copysign(limit(abs(value), minimum, maximum, False), value)
    else:
        if minimum is not None:
            value=max(value, minimum)

        if maximum is not None:
            value=min(value, maximum)
            
        return value

class System:
    pass

class P(System):
    def __init__(self, K=1):
        self._K=K
        self._y=0
        
    def update(self, dt, u):
        self._y=u

    def output(self):
        # Return state
        return self._y
    

class PT1(System):
    def __init__(self, T, K=1):
        # Initialize parameters
        self._T = T
        self._K = K
        
        # Initialize state
        self._y = 0
    
    def update(self, dt, u):
        # Fetch parameters
        K = self._K
        T = self._T
        
        #Update state
        y = self._y
        y = 1 / (T / dt + 1) * (K * u + T / dt * y)
        self._y = y

    def output(self):
        # Return state
        return self._y

class Motor(System):
    def __init__(self, friction, acceleration):
        self._friction = friction
        self._acceleration = acceleration
        
        self._speed=0
        
    def update(self, dt, u):
        power = u
        
        acceleration = power * self._acceleration - self._friction * self._speed
        self._speed += acceleration * dt
    
    def output(self):
        return self._speed

class RateLimiter(System):
    def __init__(self, max_rate, max_value):
        self._max_rate =max_rate
        self._max_value=max_value
        
        self._value=0
        
    def update(self, dt, u):
        target=u
        
        limit_delta = dt * self._max_rate

        requested_value = limit(target, maximum=self._max_value, absolute=True)
        requested_delta = requested_value - self._value
        limited_delta = limit(requested_delta, maximum = limit_delta, absolute=True)

        self._value += limited_delta
    
    def output(self):
        return self._value
    
class ChainSystem(System):
    def __init__(self, systems):
        self._systems = systems
        
        self._output = 0
    
    def update(self, dt, u):
        for system in self._systems:
            system.update(dt, u)
            u=system.output()
            
        self._output=u

    def output(self):
        return self._output
        
        


if __name__ == '__main__':
    #system=P(1)
    #system=PT1(1, 1)
    #system=Motor(1, 1)
    #system=RateLimiter(0.5, 0.8)
    system=ChainSystem([PT1(0.5,1), PT1(0.5,1)])

    time = 5
    dt = 1/50

    def u(t):
        if t>=1:
            return 1
        else:
            return 0

    T=np.arange(0, time+dt, dt)
    
    Y=np.zeros(np.size(T))
     
    Y[0]=system.output()
    previous_t=T[0]
    for i, t in enumerate(T[1:]):
        system.update(dt, u(t))
        Y[i+1]=system.output()

    plt.plot(T, Y, '.-')
    plt.show()
