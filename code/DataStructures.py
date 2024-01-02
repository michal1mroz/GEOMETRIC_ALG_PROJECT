"""
    This file contains all the data structures used in the program.
    Implemented:
    - Point
    - Segment
    - Trapezoid
    - DNode
    - DTree
"""


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __gt__(self, other):
        return self.x > other.x

    def toTuple(self):
        return self.x, self.y

    def __str__(self):
        return self.x + "," + self.y


class Segment:
    def __init__(self, p, q):
        self.left = p
        self.right = q
        if q < p:
            self.left = q
            self.right = p

        if self.left.x != self.right.x:
            self.m = (self.left.y - self.right.y) / (self.left.x - self.right.x)
            self.b = self.left.y - (self.m * self.left.x)

        else:
            self.m = None
            self.b = None

    def __gt__(self,other):
        return self.m*Segment.x+self.b>other.m*Segment.x+other.b
    
    def updateX(x):
        Segment.x = x

    def getY(self, x):
        if self.left.x <= x <= self.right.x:
            return (self.m * x) + self.b
        return None

    def isAbove(self, point):
        return (point.y > self.getY(point.x))

    def toTuple(self):
        return ((self.left.x, self.left.y), (self.right.x, self.right.y))

    def __str__(self):
        return str(self.left.toTuple()) + " " + str(self.right.toTuple())


class Trapezoid:
    def __init__(self, top, bottom, p, q):
        self.topSegment = top
        self.bottomSegment = bottom
        self.leftPoint = p
        self.rightPoint = q

        self.topLeft = None
        self.bottomLeft = None
        self.topRight = None
        self.bottomRight = None

        self.node = None

    def __str__(self):
        return str(self.bottomSegment) + " " + str(self.topSegment)


class DNode:
    def __init__(self, type, label):
        self.type = type
        self.label = label
        self.left = None
        self.right = None
        

class DTree:
    def __init__(self, root):
        self.root = root

    def updateRoot(self, root):
        self.root = root

    def query(self, node, point, segment=None):
        if node.type == 'tnode':
            return node.label
        if node.type == 'pnode':
            if point < node.label:
                return self.query(node.left, point, segment)
            else:
                return self.query(node.right, point, segment)
        else:
            if node.label.isAbove(point):
                return self.query(node.left, point, segment)
            elif node.label.getY(point.x) == point.y:
                if segment.m > node.label.m:
                    return self.query(node.left, point, segment)
                else:
                    return self.query(node.right, point, segment)
            else:
                return self.query(node.right, point, segment)
