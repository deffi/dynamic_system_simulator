# class Variable:
#     def __init__(self):
#         self._reference = None
#         self._value = None
#     
#     def connect(self, reference):
#         self._reference = reference
#         
#     def set(self, value):
#         if self._reference is None:
#             self._value = value
#         else:
#             self._reference.set(value)
#         
#     def get(self):
#         if self._reference is None:
#             return self._value
#         else:
#             return self._reference.get()
