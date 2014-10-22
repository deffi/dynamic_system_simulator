from variable import Variable
from variables_wrapper import VariablesWrapper


class System:
    def __init__(self, name):
        self.name = name
        self.variables = []
        self.variables_wrapper = VariablesWrapper(self)
        self.subsystems=[]
        self.parent = None

    def add_variable(self, name, initial_value = None, **kwargs):
        variable = Variable(self, name, initial_value, **kwargs)
        self.variables.append(variable)
        setattr(self, name, variable)
        return variable

    def add_input(self, name, initial_value = None, **kwargs):
        return self.add_variable(name, initial_value, **kwargs)

    def add_output(self, name, initial_value = None, **kwargs):
        return self.add_variable(name, initial_value, **kwargs)

    def add_subsystem(self, system):
        system.parent = self
        self.subsystems.append(system)
        setattr(self, system.name, system)
        return system

    def update_subsystems(self, var, t, dt):
        for subsystem in self.subsystems:
            subsystem.update(subsystem.variables_wrapper, t, dt)
        
    def update(self, var, t, dt):
        self.update_subsystems(var, t, dt)

    def full_name(self):
        if self.parent is None:
            return self.name or "?"
        else:
            return "%s.%s" % (self.parent.full_name(), self.name)

def print_system(system):
    print(system.full_name())
    for variable in system.variables:
        print("  - %s" % (variable, ))
    for subsystem in system.subsystems:
        print_system(subsystem)

if __name__ == "__main__":
    system = System("system")
    var = system.variables_wrapper
    system.add_input("inp", 9991)
    system.add_output("out", 9992)
    var.inp=1
    var.out=2
    var.inp+=0.1
    var.out+=0.1
    print(system.inp.get(), var.inp)
    print(system.out.get(), var.out)


