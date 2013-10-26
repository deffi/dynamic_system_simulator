from variable import Variable

class System:
    def __init__(self):
        self._variables={}
        self._subsystems={}

        self.setup()

    # FIXME do we need pre_update and post_update, performed before and after
    # subsystem updates?
    def do_update(self, t, dt):
        self.update(t, dt)
        for subsystem in self._subsystems.values():
            subsystem.do_update(t, dt)

    def _variable(self, name):
        variable = Variable()
        self._variables[name] = variable
        setattr(self, name, variable)
        return variable

    def update(self, t, dt):
        pass

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