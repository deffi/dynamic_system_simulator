class Variable:
    def __init__(self, name):
        self.name = name

    def value(self):
        raise NotImplementedError()

    def set_value(self, value):
        raise NotImplementedError()

class SourceVariable(Variable):
    def __init__(self, name):
        super(SourceVariable, self).__init__(name)
        self._value = None
    
    def value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        

class SinkVariable(Variable):
    def __init__(self, name):
        super(SourceVariable, self).__init__(name)
        self._reference = None
        
    def connect(self, reference):
        self._reference = reference

    def value(self):
        if self._reference:
            return self._reference.value()
        else:
            raise ValueError("Sink variable without reference")
        
    def set_value(self, value):
        if self._reference:
            self._reference.set_value(value)
        else:
            raise ValueError("Sink variable without reference")