class VariableBackend:
    def get(self):
        raise NotImplemented("get() is not implemented")
    
    def set(self, value):
        raise NotImplemented("get() is not implemented")

class ReadOnlyVariableBackend(VariableBackend):
    def set(self, value):
        raise ValueError("Read-only variable backend")

class Value(VariableBackend):
    def __init__(self, value = None):
        self._value = value
        
    def get(self):
        return self._value
    
    def set(self, value):
        self._value = value

class Sum(ReadOnlyVariableBackend):
    def __init__(self, summands):
        for summand in summands:
            if not isinstance(summand, (Variable, int, float)):
                raise ValueError("Expected Variable or numeric type, got %s" % (summand, ))
            
        self._summands = summands
        
    def get(self):
        return sum([float(summand) for summand in self._summands])

class Product(ReadOnlyVariableBackend):
    def __init__(self, factors):
        for factor in factors:
            if not isinstance(factor, (Variable, int, float)):
                raise ValueError("Expected Variable or numeric type, got %s" % (factor, ))
            
        self._factors = factors
        
    def get(self):
        result = 1
        for factor in self._factors:
            result *= float(factor)
        
        return result

class Variable(VariableBackend):
    def __init__(self, value = None):
        if isinstance(value, VariableBackend):
            self._backend = value
        else:
            self._backend = Value(value)
        
    def get(self):
        return self._backend.get()
    
    def set(self, value):
        self._backend.set(value)  

    def connect(self, backend):
        self._backend = backend

    def __float__(self):
        return float(self.get())

    def __add__(self, other):
        if not isinstance(other, (Variable, int, float)):
            raise ValueError("Expected Variable or numeric type, got %s" % (other, ))
        
        return Variable(Sum([self, other]))

    def __radd__(self, other):
        return self + other


if __name__ == '__main__':
    import unittest

    class VariableTests(unittest.TestCase):
        def testVariable(self):
            v1 = Variable(1111)
            v2 = Variable(2222)
            v3 = Variable(4444)

            self.assertEqual(v1.get(), 1111)
            self.assertEqual(v2.get(), 2222)
            self.assertEqual(v3.get(), 4444)
            self.assertEqual(float(v1), 1111)
            self.assertEqual(float(v2), 2222)
            self.assertEqual(float(v3), 4444)
        
            v1_reference = Variable()
            v1_reference.connect(v1)
            v2_reference = Variable(v2)

            self.assertEqual(v1_reference.get(), 1111)
            self.assertEqual(v2_reference.get(), 2222)
            
            v_sum = Variable(Sum([v1, v2, v3, 0.1]))
            v_product = Variable(Product([v1, v2, v3, 1.1]))
            
            v_add = v1 + v2 + v3 + 0.2
            
            self.assertEqual(v_sum.get(), 7777.1)
            self.assertEqual(v_add.get(), 7777.2)
             
            v1.set(1)
            v2_reference.set(2)
            v3.set(4)

            self.assertEqual(v1.get(), 1)
            self.assertEqual(v2.get(), 2)
            self.assertEqual(v3.get(), 4)

            self.assertEqual(v_sum.get(), 7 + 0.1)
            self.assertEqual(v_product.get(), 8 * 1.1)
            
            self.assertRaises(ValueError, lambda: v_sum.set(1))
            self.assertRaises(ValueError, lambda: v_add.set(1))

    unittest.main()
