class Variable():
    def __init__(self, name, value = None):
        self._name = name
        self._value = value
        
    def name(self):
        return self._name
        
    def set(self, value):
        self._value = value

    def get(self):
        return self._value

    def __str__(self):
        return "%s = %s" % (self._name, self._value)
    
    def __repr__(self):
        return "Variable(%s, %s)" % (self._name, self._value)



class System:
    def __init__(self):
        self._inputs=[]     # List of input names
        self._outputs=[]    # List of output names
        self._subsystems=[] # List of subsystem names

    def add_variable(self, name, initial_value = None):
        variable = Variable(name, initial_value)
        setattr(self, name, variable)
        return variable

    def add_input(self, name, initial_value = None):
        self.add_variable(name, initial_value)
        self._inputs.append(name)

    def add_output(self, name, initial_value = None):
        self.add_variable(name, initial_value)
        self._outputs.append(name)

    def add_subsystem(self, name, system):
        self._subsystems.append(name)
        setattr(self, name, system)

    def update_subsystems(self, t, dt):
        for subsystem in self._subsystems:
            getattr(self, subsystem).update(t, dt)
        
    def update(self, t, dt):
        self.update_subsystems(t, dt)
