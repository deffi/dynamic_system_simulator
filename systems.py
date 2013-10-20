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



# v2
#
# class Integrator(System):
#     def setup(self):
#         self.input("input")
#         self.output("output")
#         
#     def initialize(self):
#         self.i=0
#         
#     def step(self, dt, input_):
#         self.output += self.input * dt
# 
# class Gain(System):
#     def setup(self):
#         self.input("input")
#         self.output("output")
#         self.parameter("gain")
#     
#     def initialize(self):
#         pass
#         
#     def update(self, t, dt):
#         self.output = self.gain * self.input

# v1
#
# class P(System):
#     def __init__(self, K=1):
#         self._K=K
#         self._y=0
#         
#     def update(self, dt, u):
#         self._y=self._K*u
# 
#     def output(self):
#         # Return state
#         return self._y
# 
# class PController(P):
#     def __init__(self, p_gain=1):
#         P.__init__(self, -p_gain)
# 
# class PIDController(System):
#     def __init__(self, p_gain, i_gain, d_gain):
#         self._p_gain = p_gain
#         self._i_gain = i_gain
#         self._d_gain = d_gain
# 
#         self._i_error = 0
#         self._previous_error = None        
#         
#     def update(self, dt, u):
#         error = u
#         
#         # Calculate the error components - P
#         p_error = error
# 
#         # Calculate the error components - I
#         self._i_error += error * dt
#         #if self._i_term_max is not None:
#         #    self._i_error = limit(self._i_error, maximum = self._i_term_max / i_gain, absolute = True)
#         #if sign(self._i_error) != sign(error):
#         #    self._i_error = 0
#         i_error = self._i_error
# 
#         # Calculate the error components - D
#         if self._previous_error is None:
#             d_error = 0
#         else:
#             d_error = (error - self._previous_error) / dt
#         self._previous_error = error
# 
#         # Calculate the controller terms
#         p_term = self._p_gain * p_error
#         i_term = self._i_gain * i_error
#         d_term = self._d_gain * d_error
# 
#         # Calculate the output
#         self._p_term = - p_term
#         self._i_term = - i_term
#         self._d_term = - d_term
#         self._output = - p_term - i_term - d_term
# 
#     def output(self):
#         # Return state
#         return self._output
# 
# class Integrator(System):
#     def __init__(self):
#         self._value = 0
#         
#     def update(self, dt, u):
#         self._value += dt * u
#         
#     def output(self):
#         return self._value    
#     
# 
# class PT1(System):
#     def __init__(self, T, K=1):
#         # Initialize parameters
#         self._T = T
#         self._K = K
#         
#         # Initialize state
#         self._y = 0
#     
#     def update(self, dt, u):
#         # Fetch parameters
#         K = self._K
#         T = self._T
#         
#         #Update state
#         y = self._y
#         y = 1 / (T / dt + 1) * (K * u + T / dt * y)
#         self._y = y
# 
#     def output(self):
#         # Return state
#         return self._y
# 
# class Motor(System):
#     def __init__(self, friction, acceleration, static_friction):
#         self._friction = friction
#         self._acceleration = acceleration
#         self._static_friction = static_friction
#         
#         self._speed=0
#         
#     def update(self, dt, u):
#         power = u
# 
#         if abs(power) < self._static_friction:
#             power = 0
#             
#         acceleration = power * self._acceleration - self._friction * self._speed
#         self._speed += acceleration * dt
#             
#     
#     def output(self):
#         return self._speed
# 
# class RateLimiter(System):
#     def __init__(self, max_rate, max_value):
#         self._max_rate =max_rate
#         self._max_value=max_value
#         
#         self._value=0
#         
#     def update(self, dt, u):
#         target=u
#         
#         limit_delta = dt * self._max_rate
# 
#         requested_value = limit(target, maximum=self._max_value, absolute=True)
#         requested_delta = requested_value - self._value
#         limited_delta = limit(requested_delta, maximum = limit_delta, absolute=True)
# 
#         self._value += limited_delta
#     
#     def output(self):
#         return self._value
#     
# class ChainSystem(System):
#     def __init__(self, systems):
#         self._systems = systems
#         
#         self._output = 0
#     
#     def update(self, dt, u):
#         for system in self._systems:
#             system.update(dt, u)
#             u=system.output()
#             
#         self._output=u
# 
#     def output(self):
#         return self._output
# 
# class PT2(ChainSystem):
#     def __init__(self, T, K=1):
#         K=math.sqrt(K)
#         ChainSystem.__init__(self, [PT1(T, K), PT1(T, K)])
# 
# class DualIntegrator(ChainSystem):
#     def __init__(self):
#         ChainSystem.__init__(self, [Integrator(), Integrator()])
# 
# 
# 
# class ControlledSystem(System):
#     def __init__(self, system, controller):
#         self._system     = system
#         self._controller = controller        
#         
#     def update(self, dt, u):
#         e = self._system.output() - u
#         self._controller.update(dt, e)
#         print(e, self._controller.output())
#         self._system.update(dt, self._controller.output())
#     
#     def output(self):
#         return self._system.output()
