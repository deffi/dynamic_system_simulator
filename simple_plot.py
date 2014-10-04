import math
from collections import namedtuple

Range = namedtuple("range", ("min", "max"))


def minmax(range_list):
    min_max = list(zip(*range_list))
    return Range(min(min_max[0]), max(min_max[1]))

class Series:
    def __init__(self, x, y, character = "#"):
        self._x = x
        self._y = y
        self._character = character
        
    def x_range(self):
        return Range(min(self._x), max(self._x))
    
    def y_range(self):
        return Range(min(self._y), max(self._y))
        

class SimplePlot:
    def __init__(self):
        self._series = []
    
    def plot(self, x, y, character = '#'):
        self._series.append(Series(x, y, character))
    
    def render(self, w = 80, h = 25, background = "·"):
        area = [[background for _ in range(w)] for _ in range(h)]

        x_range = minmax([series.x_range() for series in self._series])
        y_range = minmax([series.y_range() for series in self._series])
        
        for series in self._series:
            for xx, yy in zip(series._x, series._y):
                ix = (w-1)*(xx-x_range.min)/(x_range.max-x_range.min)
                iy = (h-1)*(yy-y_range.min)/(y_range.max-y_range.min)
                area[round(iy)][round(ix)] = series._character

        return area

    def to_string(self, *args, **kwargs):
        area = self.render(*args, **kwargs)
        return "\n".join(["".join(line) for line in reversed(area)])

    def dump(self, *args, **kwargs):
        print(self.to_string(*args, **kwargs))


def plot(x, y, w, h):
    p=SimplePlot(w, h)
    p.plot(x, y)
    p.dump()

if __name__ == "__main__":
    x = [0.1*x for x in range(100)]
    y1 = [math.sin(x) for x in x]
    y2 = [math.cos(x) for x in x]

    p=SimplePlot()
    p.plot(x, y1)
    p.plot(x[30:50], y2[30:50], character="*")
    p.dump(w=80, h=15)
