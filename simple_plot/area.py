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
    '''
    A rectangular character drawing area.
    
    An area consists of a two-dimensional array of characters. Coordinates
    (x, y) refer to characters, not character corners. The coordinates of the
    lower left corner are (0, 0), and the coordinates of the upper right corner
    are (width-1, height-1).
    
    This class is abstract; implementations must implement the do_paint method
    which performs the actual painting.
    '''
    def __init__(self, width, height):
        '''
        Initializes an area with a given width and height.
        '''
        self._width = width
        self._height = height

    def is_inside(self, p):
        '''
        Returns true if the coordinates (given as tuple p = (x, y)) are inside
        the drawing area.  
        '''
        x, y = p
        return x >= 0 and y >= 0 and x < self._width and y < self._height

    def paint(self, p, character, ignore_outside = False):
        '''
        Sets the character at coordinates p = (x, y) to the specified character.
        If the coordinates are not integer, they will be rounded.

        If ignore_outside is truthy, coordinates outside the drawing area are
        ignored. Otherwise, an exception of type ValueError is raised.
        '''
        if not self.is_inside(p):
            if ignore_outside:
                return
            else:
                raise ValueError("Point %s is outside the area %s" % (p, (self._width, self._height)))

        x, y = p
        self.do_paint(int(round(x)), int(round(y)), character)

    def paint_text(self, p, text, ignore_outside = False):
        '''
        Paints text, starting at the given position p = (x, y), and extending
        to the right (positive x direction).

        If ignore_outside is truthy, any text that ends up outside the drawing
        area is ignored. Otherwise, an exception of type ValueError is raised.
        '''
        x, y = p
        for i in range(len(text)):
            self.paint((x + i, y), text[i], ignore_outside)
        
    def paint_horizontal_line(self, y, character, ignore_outside = False):
        '''
        Paints all cells with the specified y coordinate with the specified
        character.

        If ignore_outside is truthy, coordinates outside the drawing area are
        ignored. Otherwise, an exception of type ValueError is raised.
        '''
        for x in range(self._width):
            self.paint((x, y), character, ignore_outside)

    def paint_vertical_line(self, x, character, ignore_outside = False):
        '''
        Paints all cells with the specified x coordinate with the specified
        character.

        If ignore_outside is truthy, coordinates outside the drawing area are
        ignored. Otherwise, an exception of type ValueError is raised.
        '''
        for y in range(self._height):
            self.paint((x, y), character, ignore_outside)

    def paint_cross(self, p, ignore_outside = False):
        '''
        Paints a cross with line drawing characters. The cross extends along the
        whole width and height of the drawing area, with the center at p. 

        If ignore_outside is truthy, coordinates outside the drawing area are
        ignored. Otherwise, an exception of type ValueError is raised.
        '''
        x, y = p
        self.paint_horizontal_line(y, hline, ignore_outside)
        self.paint_vertical_line(x, vline, ignore_outside)
        self.paint(p, cross, ignore_outside)

    def paint_frame(self, corner = None, size = None, ignore_outside = False):
        '''
        Paints a frame with line drawing characters. The lower left corner of
        the frame is located at corner = (x, y), and the size of the frame is
        specified by size = (width, height). The specified size describes the
        total size of the frame; the size of the inner area will be two
        characters smaller in each direction. The minimum size is (2, 2).  

        If ignore_outside is truthy, coordinates outside the drawing area are
        ignored. Otherwise, an exception of type ValueError is raised.
        '''
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

    def sub_area(self, offset, width, height):
        '''
        Returns a proxy for a sub-area (see AreaProxy).
        
        The offset is the lower left corner.
        '''
        return AreaProxy(self, offset, width, height)
    
    def shrink(self, margin):
        '''
        A front-end to sub_area, this returns a sub-area that is smaller than
        self by margin on every side (left, right, to, bottom). Consequently,
        the width and height of the returned sub-area are smaller than the width
        and height of this area, respectively, by twice the margin.  
        '''
        return self.sub_area((margin, margin), self._width-2*margin, self._height-2*margin)


class Area(AbstractArea):
    '''
    The default implementation of AbstractArea, which paints to a list of
    strings and allows rendering to a multi-line string.
    '''
    def __init__(self, width, height, background):
        '''
        Creates an area of given width and height, filled with the background
        character. background must be a single-character string.
        '''
        super(Area, self).__init__(width, height)
        self._area = [[background for _ in range(width)] for _ in range(height)]

    def do_paint(self, x, y, character):
        self._area[y][x] = character

    def to_string(self):
        '''
        Renders an area to a string. The string will consist of a number of
        lines given by the height of the area, each consisting of a number of
        characters given by the width of the area.
        '''
        return "\n".join(["".join(line) for line in reversed(self._area)])


class AreaProxy(AbstractArea):
    '''
    An area which paints to a region of another area.
    '''
    def __init__(self, target, offset, width, height):
        '''
        Creates an area proxy with the given target. Position (0, 0) in the area
        proxy maps to position offset in the target. The x and y directions are
        the same as in the target.
        '''
        super(AreaProxy, self).__init__(width, height)
        self._target = target
        self._offset = offset

    def do_paint(self, x, y, character):
        # Transform the coordinates and forward to the do_paint method of the
        # target.
        self._target.do_paint(x + self._offset[0], y + self._offset[1], character)
