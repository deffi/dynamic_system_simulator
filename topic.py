class Topic:
    def __init__(self):
        self.value=None

    def set_value(self, value):
        self._value = value
        
    def value(self):
        return self._value
