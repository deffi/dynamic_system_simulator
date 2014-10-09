from variable import Variable

class Container:
    pass

class System:
    def __init__(self):
        self.variables = Container()
        self.subsystems=[]
        self.name = None
        self.parent = None

    def add_variable(self, name, initial_value = None):
        variable = Variable(self, name, initial_value)
        setattr(self.variables, name, variable)
        return variable

    def add_input(self, name, initial_value = None):
        self.add_variable(name, initial_value)

    def add_output(self, name, initial_value = None):
        self.add_variable(name, initial_value)

    def add_subsystem(self, name, system):
        system.name = name
        system.parent = self
        self.subsystems.append(system)
        setattr(self, name, system)

    def update_subsystems(self, t, dt):
        for subsystem in self.subsystems:
            subsystem.update(t, dt)
        
    def update(self, t, dt):
        self.update_subsystems(t, dt)

    def full_name(self):
        if self.parent is None:
            return self.name or "?"
        else:
            return "%s.%s" % (self.parent.full_name(), self.name)

    def __setattr__(self, name, value):
#         variables = getattr(self, "variables")
#         if hasattr(variables, name):
#             variable = getattr(variables, name)
#             variable.set(value)
#         else:
#             super(System, self).__setattr__(name, value)

        # Geht
        if "variables" in self.__dict__:
            variables = self.variables
            if hasattr(variables, name):
                variable = getattr(variables, name)
                variable.set(value)
                return
  
        super(System, self).__setattr__(name, value)

    def __getattr__(self, name):
        variables = self.__dict__["variables"]
        if hasattr(variables, name):
            variable = getattr(variables, name)
            return variable.get()
        else:
            return super(System, self).__getattr__(name)

def print_system(system):
    print(system.full_name())
    for variable in system.variables.__dict__.values():
        print("  - %s" % (variable, ))
    for subsystem in system.subsystems:
        print_system(subsystem)
