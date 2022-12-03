"""
author: Xiaohan Wu
NYU ID: xw2788
email: xw2788@nyu.edu
"""

class Point:
    def __init__(self, v, name='') -> None:
        self.vector = v
        self.name = name

    def e2distance(self, _o):
        return sum([(x-y)**2 for x, y in zip(self.vector, _o.vector)])

    def manhdistance(self, _o):
        return sum([abs(x-y) for x, y in zip(self.vector, _o.vector)])
    
    def __add__(self, _o):
        return Point([x+y for x, y in zip(self.vector, _o.vector)])
    
    def __truediv__(self, _o):
        if not isinstance(_o, int):
            raise Exception("point object cannot be divided by non-int")
        if _o == 0:
            raise ZeroDivisionError
        return Point([ x/_o for x in self.vector ])

    def __eq__(self, __o: object) -> bool:
        return sum([0 if x == y else 1 for x, y in zip(self.vector, __o.vector)]) == 0
    
    def __str__(self) -> str:
        return f"({', '.join([str(i) for i in self.vector])})"

    def __repr__(self) -> str:
        if self.name:
            return self.name
        return self.__str__()

