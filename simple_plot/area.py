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

    def paint_cross(self, p, ignore_outside = False):
        x, y = p
        self.paint_horizontal_line(y, hline, ignore_outside)
        self.paint_vertical_line(x, vline, ignore_outside)
        self.paint(p, cross, ignore_outside)

    def paint_frame(self, corner, size, ignore_outside = False):
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

