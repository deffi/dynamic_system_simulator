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
        self._y=self._K*u

    def output(self):
        # Return state
        return self._y

class PController(P):
    def __init__(self, p_gain=1):
        P.__init__(self, -p_gain)

class PIDController(System):
    def __init__(self, p_gain, i_gain, d_gain):
        self._p_gain = p_gain
        self._i_gain = i_gain
        self._d_gain = d_gain

        self._i_error = 0
        self._previous_error = None        
        
    def update(self, dt, u):
        error = u
        
        # Calculate the error components - P
        p_error = error

        # Calculate the error components - I
        self._i_error += error * dt
        #if self._i_term_max is not None:
        #    self._i_error = limit(self._i_error, maximum = self._i_term_max / i_gain, absolute = True)
        #if sign(self._i_error) != sign(error):
        #    self._i_error = 0
        i_error = self._i_error

        # Calculate the error components - D
        if self._previous_error is None:
            d_error = 0
        else:
            d_error = (error - self._previous_error) / dt
        self._previous_error = error

        # Calculate the controller terms
        p_term = self._p_gain * p_error
        i_term = self._i_gain * i_error
        d_term = self._d_gain * d_error

        # Calculate the output
        self._p_term = - p_term
        self._i_term = - i_term
        self._d_term = - d_term
        self._output = - p_term - i_term - d_term

    def output(self):
        # Return state
        return self._output

class Integrator(System):
    def __init__(self):
        self._value = 0
        
    def update(self, dt, u):
        self._value += dt * u
        
    def output(self):
        return self._value    
    

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
    def __init__(self, friction, acceleration, static_friction):
        self._friction = friction
        self._acceleration = acceleration
        self._static_friction = static_friction
        
        self._speed=0
        
    def update(self, dt, u):
        power = u

        if abs(power) < self._static_friction:
            power = 0
            
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

class PT2(ChainSystem):
    def __init__(self, T, K=1):
        K=math.sqrt(K)
        ChainSystem.__init__(self, [PT1(T, K), PT1(T, K)])

class DualIntegrator(ChainSystem):
    def __init__(self):
        ChainSystem.__init__(self, [Integrator(), Integrator()])



class ControlledSystem(System):
    def __init__(self, system, controller):
        self._system     = system
        self._controller = controller        
        
    def update(self, dt, u):
        e = self._system.output() - u
        self._controller.update(dt, e)
        print(e, self._controller.output())
        self._system.update(dt, self._controller.output())
    
    def output(self):
        return self._system.output()


if __name__ == '__main__':
    #system=P(1)
    #system=PT1(1, 1)
    #system=PT2(1, 1)
    #system=Integrator()
    #system=DualIntegrator()
    #system=Motor(1, 1, 0.05)
    #system=RateLimiter(0.5, 0.8)
    #system=ChainSystem([PT1(0.5,1), PT1(0.5,1)])
    #system=ControlledSystem(Integrator(), PController(1))
    #system=ControlledSystem(DualIntegrator(), PController(1))
    #system=ControlledSystem(PT1(1, 1), PController(1))
    #system=ControlledSystem(PT2(1, 1), PController(1))

    #wheel_system=ChainSystem([RateLimiter(1, 1), Motor(1, 1, 0.1), Integrator()])
    wheel_system=ChainSystem([Motor(1, 1, 0.1), Integrator()])
    #system=ControlledSystem(wheel_system, PController(1))
    system=ControlledSystem(wheel_system, PIDController(1, 0.1, 0.5))


    time = 20
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

    plt.plot(T, Y, '-')
    plt.grid()
    plt.show()
