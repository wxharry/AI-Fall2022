"""
author: Xiaohan Wu
NYU ID: xw2788
email: xw2788@nyu.edu
"""

class Point:
    def __init__(self, v) -> None:
        self.vector = v

    def e2distance(self, _o):
        return sum([(x-y)**2 for x, y in zip(self.vector, _o.vector)])

    def manhdistance(self, _o):
        return sum([(x-y) for x, y in zip(self.vector, _o.vector)])
    

