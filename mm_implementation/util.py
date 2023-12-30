import random
from DataStructures import *


def orient(p1, p2, p3, eps=10**(-10)):
    det = p1[0] * p2[1] + p1[1] * p3[0] + p2[0] * p3[1] - p2[1]*p3[0] - p1[1]*p2[0] - p1[0]*p3[1]
    return 1 if det > eps else 2


def intersect(l1, l2):
    p1 = l1[0]
    q1 = l1[1]
    p2 = l2[0]
    q2 = l2[1]
    return orient(p1, q1, p2) != orient(p1, q1, q2) and orient(p2, q2, p1) != orient(p2, q2, q1)


def permute(S):
    return random.sample(S, len(S))


def updateLeft(old, new):
    if old.topLeft:
        if old.topLeft.topRight == old:
            old.topLeft.topRight = new
        if old.topLeft.bottomRight == old:
            old.topLeft.bottomRight = new
    if old.bottomLeft:
        if old.bottomLeft.topRight == old:
            old.bottomLeft.topRight = new
        if old.bottomLeft.bottomRight == old:
            old.bottomLeft.bottomRight = new


def updateRight(old, new):
    if old.topRight:
        if old.topRight.topLeft == old:
            old.topRight.topLeft = new
        if old.topRight.bottomLeft == old:
            old.topRight.bottomLeft = new
    if old.bottomRight:
        if old.bottomRight.topLeft == old:
            old.bottomRight.topLeft = new
        if old.bottomRight.bottomLeft == old:
            old.bottomRight.bottomLeft = new


def findIntersectTrapezoids(start, segment, intersects):
    current = start
    intersects.clear()
    intersects.append(current)
    while segment.rightPoint.x > current.rightPoint.x:
        if current.rightPoint.y <= segment.getY(current.rightPoint.x):
            current = current.topRight
        else:
            current = current.bottomRight
        intersects.append(current)


def bounds(lines):
    x1 = min(lines, key=lambda x: x[0][0])[0][0]
    x2 = max(lines, key=lambda x: x[1][0])[1][0]
    y1 = min(lines, key=lambda x: x[0][1])[0][1]
    y2 = min(lines, key=lambda x: x[1][1])[1][1]
    y3 = max(lines, key=lambda x: x[0][1])[0][1]
    y4 = max(lines, key=lambda x: x[1][1])[1][1]

    if y1 > y2:
        y1 = y2
    if y3 < y4:
        y3 = y4

    bx = (x2-x1)/10
    by = (y3-y1)/10

    return x1-bx, x2+bx, y1-by, y3+by


def createOuter(lines):
    x1, x2, y1, y2 = bounds(lines)
    lowLeft = Point(x1, y1)
    lowRight = Point(x2, y1)
    upRight = Point(x2, y2)
    upLeft = Point(x1, y2)
    topSegment = Segment(upLeft, upRight)
    bottomSegment = Segment(lowLeft, lowRight)
    return Trapezoid(topSegment, bottomSegment, upLeft, upRight)

