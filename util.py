import math

def limit(value, minimum=None, maximum=None, absolute=False):
    if absolute:
        return math.copysign(limit(abs(value), minimum, maximum, False), value)
    else:
        if minimum is not None:
            value=max(value, minimum)

        if maximum is not None:
            value=min(value, maximum)
            
        return value
