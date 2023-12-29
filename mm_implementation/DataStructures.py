'''

    This file contains all the data structures used in the program.
    Implemented:
    - Point
    - Segment
    - Trapezoid
    - pnode
    - snode
    - tnode

'''


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Segment:
    def __init__(self, p, q):
        self.leftPoint = p
        self.rightPoint = q
        if q.x < p.x:
            self.leftPoint = q
            self.rightPoint = p

        self.m = (self.leftPoint.y - self.rightPoint.y) / (self.leftPoint.x - self.rightPoint.x)
        self.b = self.leftPoint.y - (self.m * self.leftPoint.x)

    def getY(self, x):
        if self.leftPoint.x <= x <= self.rightPoint.x:
            return (self.m * x) + self.b
        return None

    def isAbove(self, point):
        return point.y > self.getY(point.x)

    def toTuple(self):
        return ((self.leftPoint.x, self.leftPoint.y), (self.rightPoint.x, self.rightPoint.y))


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


class Pnode: # Point node in search tree
    def __init__(self, point, left=None, right=None):
        self.type = 'pnode'
        self.setLeft(left)
        self.setRight(right)
        self.point = point

    def setLeft(self, node):
        self.left = node
        if node is None:
            return
        if node.type == 'tnode' and self not in node.parents:
            node.parents.append(self)

    def setRight(self, node):
        self.right = node
        if node is None:
            return
        if node.type == 'tnode' and self not in node.parents:
            node.parents.append(self)


class Snode:
    def __init__(self, segment, above=None, below=None):
        self.type = 'snode'
        self.setAbove(above)
        self.setBelow(below)
        self.segment = segment

    def setAbove(self, node):
        self.above = node
        if node is None:
            return
        if node.type == 'tnode' and self not in node.parents:
            node.parents.append(self)

    def setBelow(self, node):
        self.below = node
        if node is None:
            return
        if node.type == 'tnode' and self not in node.parents:
            node.parents.append(self)


class Tnode:
    def __init__(self, trap):
        self.type = 'tnode'
        self.parents = []
        self.trapezoid = trap
        self.trapezoid.node = self

    def replaceNode(self, sg, node):
        if not self.parents:
            sg.updateRoot(node)
            return
        for parent in self.parents:
            if parent.type == 'pnode':
                if parent.left == self:
                    parent.setLeft(node)
                else:
                    parent.setRight(node)
            else:
                if parent.above == self:
                    parent.setAbove(node)
                else:
                    parent.setBelow(node)


class TrapezoidMap:
    def __init__(self, root):
        self.root = root

    def updateRoot(self, root):
        self.root = root

    def query(self, point, node=None):
        if node is None:
            node = self.root

        if node.type == 'tnode':
            return node.trapezoid
        if node.type == 'pnode':
            if point.x < node.point.x:
                return self.query(point, node.left)
            else:
                return self.query(point, node.right)
        else:
            if point.y > node.segment.getY(point.x):
                return self.query(point, node.above)
            else:
                return self.query(point, node.below)

