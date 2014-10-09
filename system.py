from variable import Variable

class Variable():
    def __init__(self, value = None):
        self._value = value
        
    def set(self, value):
        self._value = value

    def get(self):
        return self._value
    
        
        

class System:
    def __init__(self):
        self._variables={}
        self._subsystems={}

        self.setup()

    def _variable(self, name):
        variable = Variable()
        self._variables[name] = variable
        setattr(self, name, variable)
        return variable

    def subsystem(self, name, system):
        self._subsystems[name] = system
        setattr(self, name, system)

    def parameter(self, name, default_value):
        self._variable(name).set(default_value)

    def input(self, name):
        self._variable(name)
         
    def output(self, name):
        self._variable(name)
        
    def internal(self, name, initial_value):
        self._variable(name).set(initial_value)
        
    def connect(self, a, b):
        a.connect(b)
        
    def update(self, t, dt):
        for subsystem in self._subsystems.values():
            subsystem.update(t, dt)


#     def getx(self):
#         return self._x
#     def setx(self, value):
#         self._x = value
#     def delx(self):
#         del self._x
#     x = property(getx, setx, delx, "I'm the 'x' property.")
#     