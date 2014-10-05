import math
from collections import namedtuple

# TODO:
#   * verify that the area is wide enough for legend and plot area

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
    def __init__(self, x, y, character = "#", label = None):
        self._x = x
        self._y = y
        self._character = character
        self._label = label
        
    def x_range(self):
        return Range(min(self._x), max(self._x))
    
    def y_range(self):
        return Range(min(self._y), max(self._y))

class LegendEntry(namedtuple("LegendEntry", ("character", "label"))):
    def format(self):
        return "%s %s" % (self.character, self.label)
        
    def length(self):
        return len(self.format())

class Legend(list):
    def empty(self):
        return len(self) == 0
        
    def length(self):
        return max([entry.length() for entry in self])
    
    def size(self):
        width = self.length()
        height = len(self)
        return (width, height)

    def render(self, area):
        height = len(self)
        for index, entry in enumerate(self):
            area.paint_text((0, height - 1 - index), entry.format())
    

class SimplePlot:
    def __init__(self):
        self._series = []
    
    def plot(self, x, y, character = '#', label = None):
        self._series.append(Series(x, y, character, label))
    
    def render(self, w = 80, h = 25, background = "·"):
        x_range = minmax([series.x_range() for series in self._series])
        y_range = minmax([series.y_range() for series in self._series])

        area = Area(w, h, background)
 
        # Construct the legend
        legend = Legend()
        for series in self._series:
            if series._label is not None:
                legend.append(LegendEntry(series._character, series._label))
 
        # Calculate the layout
        if legend.empty():
            render_legend = False
            plot_area_width = area._width
        else:
            render_legend = True
            legend_width, legend_height = legend.size()
            legend_width += 2
            legend_height += 2
            plot_area_width = area._width - legend_width
            legend_x = plot_area_width
            legend_y = math.ceil((area._height - legend_height)/2)
 
        plot_area = area.sub_area((0, 0), plot_area_width, area._height)
        plot_area.paint_frame()
        plot_area = plot_area.shrink(1)

        if render_legend:
            legend_area = area.sub_area((legend_x, legend_y), legend_width, legend_height)
            legend_area.paint_frame()
            legend_area = legend_area.shrink(1)
            legend.render(legend_area)

        def transform(p):
            x, y = p
            tx = (plot_area._width-1)*(x-x_range.min)/(x_range.max-x_range.min)
            ty = (plot_area._height-1)*(y-y_range.min)/(y_range.max-y_range.min)
            return (tx, ty)
   
        plot_area.paint_cross(transform((0, 0)), ignore_outside = True)
        for series in self._series:
            for x, y in zip(series._x, series._y):
                plot_area.paint(transform((x, y)), series._character)


        return area

    def to_string(self, *args, **kwargs):
        return self.render(*args, **kwargs).to_string()

    def dump(self, *args, **kwargs):
        print(self.to_string(*args, **kwargs))




def plot(x, y, w, h, background = " ", label = None):
    p = SimplePlot()
    p.plot(x, y, label = label)
    p.dump(w, h, background)

if __name__ == "__main__":
    x = [0.1*x-1 for x in range(100)]
    y1 = [math.sin(x)+0.5 for x in x]
    y2 = [math.cos(x) for x in x]

    p=SimplePlot()
    p.plot(x, y1, label = "Sine")
    p.plot(x[30:50], y2[30:50], character="*", label = "Cosine")
    p.dump(w=82, h=17, background = " ")
