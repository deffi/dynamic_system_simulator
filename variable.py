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
