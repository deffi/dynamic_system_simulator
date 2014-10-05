import math
from collections import namedtuple

# FIXME better solution?
#from simple_plot.area import Area # Included as module
#from area import Area # Executed directly
if __name__ == "__main__":
    # Executing directly
    from area import Area  # @UnresolvedImport
else:
    # Included as module
    from simple_plot.area import Area

Range = namedtuple("range", ("min", "max"))

def minmax(range_list):
    mins, maxs = list(zip(*range_list))
    return Range(min(mins), max(maxs))

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

        area = Area(w, h, background)
        area.paint_frame((0, 0), (w-1, h-1))

        def transform(p):
            x, y = p
            tx = (w-2-1)*(x-x_range.min)/(x_range.max-x_range.min)
            ty = (h-2-1)*(y-y_range.min)/(y_range.max-y_range.min)
            return (tx, ty)
 
        chart_area = area.sub_area((1, 1), w-2, h-2)
        chart_area.paint_cross(transform((0, 0)), ignore_outside = True)
        for series in self._series:
            for x, y in zip(series._x, series._y):
                chart_area.paint(transform((x, y)), series._character)

        return area

    def to_string(self, *args, **kwargs):
        return self.render(*args, **kwargs).to_string()

    def dump(self, *args, **kwargs):
        print(self.to_string(*args, **kwargs))




def plot(x, y, w, h, background):
    p = SimplePlot()
    p.plot(x, y)
    p.dump(w, h, background)

if __name__ == "__main__":
    x = [0.1*x-1 for x in range(100)]
    y1 = [math.sin(x)+0.5 for x in x]
    y2 = [math.cos(x) for x in x]

    p=SimplePlot()
    p.plot(x, y1)
    p.plot(x[30:50], y2[30:50], character="*")
    p.dump(w=82, h=17, background = " ")
