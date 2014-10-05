import math
from collections import namedtuple

Range = namedtuple("range", ("min", "max"))

def minmax(range_list):
    mins, maxs = list(zip(*range_list))
    return Range(min(mins), max(maxs))

class Area:
    def __init__(self, width, height, background):
        self._width = width
        self._height = height
        self._area = [[background for _ in range(width)] for _ in range(height)]
        # Temporary hack, better solution would be a subarea proxy
        self._offset = (0, 0)

    def set_offset(self, offset):
        self._offset = offset

    def is_inside(self, p):
        x, y = p
        return x >= 0 and y >= 0 and x < self._width and y < self._height

    def paint(self, p, character, ignore_outside = False):
        'p, of course, is (x, y)'
        if not self.is_inside(p):
            if ignore_outside:
                return
            else:
                raise ValueError("Point %s is outside the area %s" % (p, (self._width, self._height)))

        x, y = p
        ox, oy = self._offset
        self._area[round(y+oy)][round(x+ox)] = character

    def paint_horizontal_line(self, y, character, ignore_outside = False):
        for x in range(self._width):
            self.paint((x, y), character, ignore_outside)

    def paint_vertical_line(self, x, character, ignore_outside = False):
        for y in range(self._height):
            self.paint((x, y), character, ignore_outside)

    def paint_cross(self, p, horizontal_character, vertical_character, center_character, ignore_outside = False):
        x, y = p
        self.paint_horizontal_line(y, "-", ignore_outside)
        self.paint_vertical_line(x, "|", ignore_outside)
        self.paint(p, "+", ignore_outside)

    def paint_frame(self, corner, size, ignore_outside = False):
        x0, y0 = corner
        w, h = size
        for x in range(x0+1, x0+w):
            self.paint((x, y0), "-", ignore_outside)
            self.paint((x, y0+h), "-", ignore_outside)
        for y in range(y0+1, y0+h):
            self.paint((x0, y), "|", ignore_outside)
            self.paint((x0+w, y), "|", ignore_outside)
        self.paint((x0, y0), "'", ignore_outside)
        self.paint((x0+w, y0), "'", ignore_outside)
        self.paint((x0, y0+h), ".", ignore_outside)
        self.paint((x0+w, y0+h), ".", ignore_outside)

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
            x, y = p
            tx = (w-1)*(x-x_range.min)/(x_range.max-x_range.min)
            ty = (h-1)*(y-y_range.min)/(y_range.max-y_range.min)
            return (tx, ty)

        area = Area(w+2, h+2, background)
        area.paint_cross(transform((0, 0)), "-", "|", "+", ignore_outside = True)
        area.paint_frame((0, 0), (w+1, h+1))

        area.set_offset((1, 1))        
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
