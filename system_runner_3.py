import numpy as np

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
        
        for i in range(len(t)):
            for var in self.variables.keys():
                self.variables[var][i] = float(var)
         
            dt = t[i]-t[i-1] if i>0 else None
            if i>0:
                self._system.update(self._system.variables_wrapper, t[i], dt)

        self.t = t

