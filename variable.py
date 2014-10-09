class Variable():
    def __init__(self, system, name, value = None):
        self.system = system
        self.name = name
        
        self._reference = None
        self._value = value
    
    def connect(self, reference):
        self._reference = reference
        
    def set(self, value):
        if self._reference is None:
            self._value = value
        elif callable(self._reference):
            print("Warning: ignoring assignment to a callable Variable")
        else:
            print("Warning: assignment to a referenced variable")
            self._reference.set(value)

    def get(self):
        if self._reference is None:
            return self._value
        elif callable(self._reference):
            return self._reference()
        else:
            return self._reference.get()

    def full_name(self):
        return "%s.%s" % (self.system.full_name(), self.name)

    def reference_names(self):
        if self._reference is None:
            return [self.full_name()]
        elif callable(self._reference):
            return [self.full_name()] + ["[callable]"]
        else:
            return [self.full_name()] + self._reference.reference_names()

    def __str__(self):
        return "%s = %s" % (" -> ".join(self.reference_names()), self.get())
    
    def __repr__(self):
        return "Variable(%s, %s)" % (self._name, self.get())
