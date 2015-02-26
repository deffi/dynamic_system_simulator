# Printing:
# system
# system.pendulum
#   - system.pendulum.gravity -> system.gravity.value = 0
# system.pendulum.mass
#   - system.pendulum.mass.force = 0
#   - system.pendulum.mass.velocity = 0
#   - system.pendulum.mass.position = 0.1
#   - system.pendulum.mass.acceleration = 0
# system.pendulum.spring
#   - system.pendulum.spring.displacement -> system.pendulum.mass.position = 0.1
#   - system.pendulum.spring.force = 0
# system.pendulum.damper
#   - system.pendulum.damper.velocity -> system.pendulum.mass.velocity = 0
#   - system.pendulum.damper.force = 0
# system.gravity
#   - system.gravity.value = 0

# system
# |-pendulum
# | | '-gravity -> value = 0
# | |-mass
# | | |-force = 0
# | | |-velocity = 0
# | | |-position = 0.1
# | | '-acceleration = 0
# | |-spring
# | | |-displacement -> mass.position = 0.1
# | | '-force = 0
# | '-damper
# |   |-velocity -> mass.velocity = 0
# |   '-force = 0
# '-gravity
#   '-value = 0

from variable3 import SourceVariable, SinkVariable

class Clock:
    def __init__(self):
        self.t = None
        self.dt = None
        self.previous_t = None
    
    def update(self, t):
        self.previous_t = self.t
        self.t = t
        if self.t is None or self.previous_t is None:
            self.dt = None
        else:  
            self.dt = self.t - self.previous_t

class VariablesWrapper:
    def __init__(self, system):
        self._system = system
    
    def __setattr__(self, name, value):
        if name[0] == "_":
            object.__setattr__(self, name, value)
        else:
            system = self._system
            variable = getattr(system, name)
            variable.set(value)
         
    def __getattr__(self, name):
        if name[0] == "_":
            return object.__getattr__(self, name)
        else:
            system = self._system
            variable = getattr(system, name)
            return variable.get()

class System:
    def __init__(self, name):
        self.name = name

    def update(self, clock):
        raise NotImplementedError()

    def add_input(self, name):
        variable = SinkVariable(name)
        setattr(self, name, variable)

    def add_output(self, name):
        variable = SourceVariable(name)
        setattr(self, name, variable)

class CompositeSystem(System):
    def __init__(self, name):
        super(CompositeSystem, self).__init__(name)
        
        self._subsystems = []

    def add_subsystem(self, subsystem):
        self._subsystems.append(subsystem)

    def update(self, clock):
        for subsystem in self._subsystems:
            subsystem.update(clock)
