import sys
import gc


a = []
print(sys.getrefcount(a))  # 2

b = a
print(sys.getrefcount(a))  # 3

del a
print(sys.getrefcount(b))  # 2

del b


class A:
    def __init__(self):
        self.ref = None


obj1 = A()
obj2 = A()

obj1.ref = obj2
obj2.ref = obj1

del obj1, obj2

gc.collect()
