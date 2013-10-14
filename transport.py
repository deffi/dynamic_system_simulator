from topic import Topic

class Transport:
    def __init__(self):
        self._topics = {}
        
    def topic(self, name):
        if name not in self._topics:
            self._topics[name] = Topic()
            
        