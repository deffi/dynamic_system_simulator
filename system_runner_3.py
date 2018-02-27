import numpy as np

from system3 import Clock 

class SystemRunner:
    def __init__(self, system):
        self._system = system
        self.variables = {}
        self.t = None

    def add_variable(self, variable):
        self.variables[variable] = None

    def run(self, time, step):
        t = np.arange(0, time, step)
        length = np.size(t)
        
        for var in self.variables.keys():
            self.variables[var] = np.zeros(length)

        clock = Clock()
        
        for i in range(len(t)):
            for var in self.variables.keys():
                self.variables[var][i] = float(var)
        
            clock.update(t[i])
         
            if i>0:
                self._system.update(clock)

        self.t = t

