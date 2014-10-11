from collections import namedtuple

def step(t):
    if t > 0:
        return 1
    else:
        return 0
    
def rect(t):
    if t > 0 and t<1:
        return 1
    else:
        return 0

_Segment = namedtuple("_Segment", ("time", "function"))

class PieceWiseFunction:
    def __init__(self):
        self._segments = []
        
    def add_segment(self, time, function):
        self._segments.append(_Segment(time, function))

    def __call__(self, t):
        segment_start = 0
        for segment in self._segments:
            segment_end = segment_start + segment.time
                
            if t >= segment_start and t < segment_end:
                return segment.function(t - segment_start)
            else:
                segment_start = segment_end  
    
        return segment.function(t - segment_start)

