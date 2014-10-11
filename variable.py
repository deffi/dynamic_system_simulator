class Sum():
    def __init__(self, variables):
        self._variables = variables
    
    def set(self, value):
        raise(Exception("Cannot set a Sum"))
    
    def get(self):
        return sum([variable.get() for variable in self._variables])
        
    def reference_names(self):
        return []

class Product():
    def __init__(self, factors):
        self._factors = factors

    def set(self, value):
        raise(Exception("Cannot set a Product"))
    
    def get(self):
        result = 1
        for factor in self._factors:
            if isinstance(factor, Variable):
                result *= factor.get()
            else:
                result *= factor
        
        return result
        
    def reference_names(self):
        return []

    
class Variable():
    def __init__(self, system, name, value = None, verbose = False):
        self.system = system
        self.name = name
        self.verbose = verbose
         
        self._reference = None
        self._value = value
    
    def connect(self, reference):
        self._reference = reference
        
    def set(self, value):
        if self.verbose:
            print("%s <- %s" % (self.full_name(), value))
            
        if self._reference is None:
            self._value = value
        elif callable(self._reference):
            print("Warning: ignoring assignment to a callable Variable")
        else:
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
        return "Variable(%s, %s)" % (self.name, self.get())

    def __add__(self, other):
        if not isinstance(other, (Variable, Sum)):
            raise TypeError("Can only add variables to other variables")
        
        return Sum([self, other])

    def __radd__(self, other):
        return self+other

    def __mul__(self, other):
        if not isinstance(other, (float, int)):
            raise TypeError("Can only add multiply variables with numerics")
        
        return Product([self, other])
            
    def __rmul__(self, other):
        return self*other