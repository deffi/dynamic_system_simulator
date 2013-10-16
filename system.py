class System:
    def __init__(self, transport, inputs, outputs):
        pass
        #self._input_topics  = [transport.topic(name) for name in inputs ]
        #self._output_topics = [transport.topic(name) for name in outputs]
        #self.initialize()

    def input(self):
        self._inputs
        
    def update(self, dt):
        pass
        #input_values = [topic.value() for topic in self._input_topics]
        #output_values = self.step(dt, *input_values)
        #for value, topic in zip(output_values, self._output_topics):
        #    topic.set_value(value)

        
