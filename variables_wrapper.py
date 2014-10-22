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
