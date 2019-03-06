import os
import inspect

def foo(x):
    return x + 1

print(inspect.getsource(foo))

print(os.path.abspath(__file__))
