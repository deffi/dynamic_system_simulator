# ASCII
# vline = "|"
# hline = "-"
# cross = "+"
# top_left = "."
# top_right = "."
# bottom_left = "'"
# bottom_right = "'"
# up = "^"
# down = "v"
# left = "<"
# right = ">"

# Unicode
vline = "│"
hline = "─"
cross = "┼"
top_left = "┌"
top_right = "┐"
bottom_left = "└"
bottom_right = "┘"
up = "▲"
down = "▼"
left = "◄"
right = "►"


class AbstractArea:
    def __init__(self, width, height):
        self._width = width
        self._height = height

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
        self.do_paint(int(round(x)), int(round(y)), character)

    def paint_text(self, p, text, ignore_outside = False):
        x, y = p
        for i in range(len(text)):
            self.paint((x + i, y), text[i], ignore_outside)
        
    def paint_horizontal_line(self, y, character, ignore_outside = False):
        for x in range(self._width):
            self.paint((x, y), character, ignore_outside)

    def paint_vertical_line(self, x, character, ignore_outside = False):
        for y in range(self._height):
            self.paint((x, y), character, ignore_outside)

    def paint_cross(self, p, ignore_outside = False):
        x, y = p
        self.paint_horizontal_line(y, hline, ignore_outside)
        self.paint_vertical_line(x, vline, ignore_outside)
        self.paint(p, cross, ignore_outside)

    def paint_frame(self, corner = None, size = None, ignore_outside = False):
        if corner is None:
            corner = (0, 0)
        if size is None:
            size = (self._width - 1 - corner[0], self._height - 1 - corner[1])
        
        x0, y0 = corner
        w, h = size
        for x in range(x0+1, x0+w):
            self.paint((x, y0), hline, ignore_outside)
            self.paint((x, y0+h), hline, ignore_outside)
        for y in range(y0+1, y0+h):
            self.paint((x0, y), vline, ignore_outside)
            self.paint((x0+w, y), vline, ignore_outside)
        self.paint((x0, y0), bottom_left, ignore_outside)
        self.paint((x0+w, y0), bottom_right, ignore_outside)
        self.paint((x0, y0+h), top_left, ignore_outside)
        self.paint((x0+w, y0+h), top_right, ignore_outside)

    def to_string(self):
        return "\n".join(["".join(line) for line in reversed(self._area)])

    def sub_area(self, offset, width, height):
        return AreaProxy(self, offset, width, height)
    
    def shrink(self, margin):
        return self.sub_area((margin, margin), self._width-2*margin, self._height-2*margin)


class Area(AbstractArea):
    def __init__(self, width, height, background):
        super(Area, self).__init__(width, height)
        self._area = [[background for _ in range(width)] for _ in range(height)]

    def do_paint(self, x, y, character):
        self._area[y][x] = character


class AreaProxy(AbstractArea):
    def __init__(self, target, offset, width, height):
        super(AreaProxy, self).__init__(width, height)
        self._target = target
        self._offset = offset

    def do_paint(self, x, y, character):
        self._target.do_paint(x + self._offset[0], y + self._offset[1], character)
