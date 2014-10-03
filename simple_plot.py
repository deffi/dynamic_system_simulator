import math

class SimplePlot:
    '''
    Note that all plots are currently scaled to full width/height individually.
    '''
    def __init__(self, w = 80, h = 25, background = "·"):
        self._w = w
        self._h = h
        self._area = [[background for _ in range(w)] for _ in range(h)]
    
    def plot(self, x, y, character = '#'):
        x_min = min(x)    
        x_max = max(x)
        y_min = min(y)
        y_max = max(y)
    
        for xx, yy in zip(x,y):
            ix = (self._w-1)*(xx-x_min)/(x_max-x_min)
            iy = (self._h-1)*(yy-y_min)/(y_max-y_min)
            self._area[round(iy)][round(ix)] = character

    def to_string(self):
        return "\n".join(["".join(line) for line in reversed(self._area)])

    def dump(self):
        print(self.to_string())

def plot(x, y, w, h):
    p=SimplePlot(w, h)
    p.plot(x, y)
    p.dump()

if __name__ == "__main__":
    x = [0.1*x for x in range(100)]
    y1 = [math.sin(x) for x in x]
    y2 = [math.cos(x) for x in x]

    p=SimplePlot(w=80, h=15)
    p.plot(x, y1)
    p.plot(x[30:50], y2[30:50], character="*")
    p.dump()
