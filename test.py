from variable import Variable
from numpy.distutils.environment import __metaclass__
 
#class MyClass(MyBase):
#    def __init__(self):
#        pass
#MyClass.x = property(getx, setx, delx, "I'm the 'x' property.")

class MyMass:
    def update(self, t, dt):
        # Access values instead of "acutual" quantities. Will only work if we
        # don't have to actually access the actual quantities.
        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

    def update_variant(self, var, t, dt):
        # var.acceleration => the current value
        # self.acceleration => the quantity
        var.acceleration = var.force / var.mass
        var.velocity += var.acceleration * dt
        var.position += var.velocity * dt
        
class OneMetaclass(type):
    def __new__(cls, name, bases, dct):
        print("Allocating a class with metaclass OneMetaclass")
        print("  name:", name)
        print("  bases:", bases)
        print("  dct:", dct)
        return type.__new__(cls, name, bases, dct)
     
    def __init__(cls, name, bases, dct):
        print("Creating a class with metaclass OneMetaclass")
        print("  name:", name)
        print("  bases:", bases)
        print("  dct:", dct)
        super(OneMetaclass, cls).__init__(name, bases, dct)
 
class OneClass(metaclass = OneMetaclass):
    def __init__(self):
        print("Creating an object with class OneClass")
     
one_instance = OneClass()

