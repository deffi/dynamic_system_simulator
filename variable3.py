class Variable:
    def __init__(self, name):
        self.name = name

    def value(self):
        raise NotImplementedError()


class SourceVariable(Variable):
    def __init__(self, name):
        super(SourceVariable, self).__init__(name)
        self._value = None
    
    def value(self):
        self._value = None
        

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
            raise NotImplementedError()
            

