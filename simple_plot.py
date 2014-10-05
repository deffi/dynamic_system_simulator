import math
from collections import namedtuple

Range = namedtuple("range", ("min", "max"))


def minmax(range_list):
    min_max = list(zip(*range_list))
    return Range(min(min_max[0]), max(min_max[1]))

class Area:
    def __init__(self, width, height, background):
        self._width = width
        self._height = height
        self._area = [[background for _ in range(width)] for _ in range(height)]

    def is_inside(self, p):
        x = p[0]
        y = p[1]
        return x >= 0 and y >= 0 and x < self._width and y < self._height

    def paint(self, p, character, ignore_outside = False):
        'p, of course, is (x, y)'
        if not self.is_inside(p):
            if ignore_outside:
                return
            else:
                raise ValueError("Point %s is outside the area" % (p))

        x = round(p[0])
        y = round(p[1])
        self._area[y][x] = character

    def to_string(self):
        return "\n".join(["".join(line) for line in reversed(self._area)])

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
        x_range = minmax([series.x_range() for series in self._series])
        y_range = minmax([series.y_range() for series in self._series])

        def transform(p):
            x = p[0]
            y = p[1]
            tx = (w-1)*(x-x_range.min)/(x_range.max-x_range.min)
            ty = (h-1)*(y-y_range.min)/(y_range.max-y_range.min)
            return (tx, ty)

        area = Area(w, h, background)
        
        xo, yo = transform((0, 0))
        for x in range(w):
            area.paint((x, yo), "-", ignore_outside = True)
        for y in range(h):
            area.paint((xo, y), "|", ignore_outside = True)
        area.paint((xo, yo), "+", ignore_outside = True)
        
        for series in self._series:
            for x, y in zip(series._x, series._y):
                area.paint(transform((x, y)), series._character)

        return area

    def to_string(self, *args, **kwargs):
        return self.render(*args, **kwargs).to_string()

    def dump(self, *args, **kwargs):
        print(self.to_string(*args, **kwargs))




def plot(x, y, w, h):
    p=SimplePlot(w, h)
    p.plot(x, y)
    p.dump()

if __name__ == "__main__":
    x = [0.1*x-1 for x in range(100)]
    y1 = [math.sin(x)+0.5 for x in x]
    y2 = [math.cos(x) for x in x]

    p=SimplePlot()
    p.plot(x, y1)
    p.plot(x[30:50], y2[30:50], character="*")
    p.dump(w=80, h=15, background = " ")
