import numpy as np
import pandas as pd


class BasePosition:
    def __init__(self, shrs, long):
        self . shares = shrs
        self . isLong = long
        print(" calling BasePosition class constructor ")
    def __del__(self):
        print(" calling BasePosition class destructor ")
    def printPos(self):
        print(" calling printPos from Base ")
        print(self . shares)
        print(self . isLong)
class ChildPosition (BasePosition):
    def __init__(self, shrs, long, childShrs):
        self . childShares = childShrs
        BasePosition . __init__(self, shrs, long)
        print(" calling ChildPosition class constructor ")
    def __del__(self):
        print(" calling ChildPosition class destructor ")
    def printPos(self):
        print(" calling printPos from Child ")
        print(self . shares)
        print(self . isLong)
        print(self . childShares)

# basePos1 = BasePosition(100, 1)
# basePos2 = BasePosition(75, 0)

childPos1 = ChildPosition(25, 0, 5)
childPos2 = ChildPosition(150, 1, 0)
childPos3 = childPos1 + childPos2

