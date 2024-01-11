import random
from DataStructures import *
import numpy as np


def permute(S):
    return random.sample(S, len(S))


def updateLeft(old, new):
    if old.topLeft:
        old.topLeft.topRight = new

    if old.bottomLeft:
        old.bottomLeft.bottomRight = new


def updateRight(old, new):
    if old.topRight:
        old.topRight.topLeft = new

    if old.bottomRight:
        old.bottomRight.bottomLeft = new


def followSegment(T, segment):
    p, q = segment.left, segment.right
    trapezoids = []
    Segment.updateX(p.x)
    trapezoid_zero = T.query(T.root, p, segment)
    trapezoids.append(trapezoid_zero)
    j = 0

    while q > trapezoids[j].rightPoint:
        Segment.updateX(trapezoids[j].rightPoint.x)
        if segment.isAbove(trapezoids[j].rightPoint):
            trapezoids.append(trapezoids[j].bottomRight)
        else:
            trapezoids.append(trapezoids[j].topRight)
        j += 1
    return trapezoids


def updateTreeOne(trapezoid, segment, left, top, bottom, right):
    node = trapezoid.node
    if left and right:
        node.type = 'pnode'
        node.label = segment.left
        lnode = DNode('tnode', left)
        node.left = lnode
        left.node = lnode
        rnode = DNode('pnode', segment.right)
        node.right = rnode
        rrnode = DNode('tnode', right)
        rnode.right = rrnode
        right.node = rrnode
        rlnode = DNode('snode', segment)
        rnode.left = rlnode
        rllnode = DNode('tnode', top)
        rlnode.left = rllnode
        top.node = rllnode
        rlrnode = DNode('tnode', bottom)
        rlnode.right = rlrnode
        bottom.node = rlrnode
    elif not left and right:
        node.type = 'pnode'
        node.label = segment.right
        rnode = DNode('tnode', right)
        node.right = rnode
        right.node = rnode
        lnode = DNode('snode', segment)
        node.left = lnode
        llnode = DNode('tnode', top)
        lnode.left = llnode
        top.node = llnode
        lrnode = DNode('tnode', bottom)
        lnode.right = lrnode
        bottom.node = lrnode
    elif left and not right:
        node.type = 'pnode'
        node.label = segment.left
        lnode = DNode('tnode', left)
        node.left = lnode
        left.node = lnode
        rnode = DNode('snode', segment)
        node.right = rnode
        rrnode = DNode('tnode', bottom)
        rnode.right = rrnode
        bottom.node = rrnode
        rlnode = DNode('tnode', top)
        rnode.left = rlnode
        top.node = rlnode
    else:
        node.type = 'snode'
        node.label = segment
        lnode = DNode('tnode', top)
        node.left = lnode
        top.node = lnode
        rnode = DNode('tnode', bottom)
        node.right = rnode
        bottom.node = rnode


def updateTreeMany(trapezoids, segment, newTrapezoidsAbove, newTrapezoidsBelow, left, right):
    node = trapezoids[0].node
    if left:
        node.type = 'pnode'
        node.label = segment.left
        lnode = DNode('tnode', left)
        node.left = lnode
        left.node = lnode
        rnode = DNode('snode', segment)
        node.right = rnode
        rlnode = DNode('tnode', newTrapezoidsAbove[0])
        rnode.left = rlnode
        newTrapezoidsAbove[0].node = rlnode
        rrnode = DNode('tnode', newTrapezoidsBelow[0])
        rnode.right = rrnode
        newTrapezoidsBelow[0].node = rrnode
    else:
        node.type = 'snode'
        node.label = segment
        lnode = DNode('tnode', newTrapezoidsAbove[0])
        node.left = lnode
        newTrapezoidsAbove[0].node = lnode
        rnode = DNode('tnode', newTrapezoidsBelow[0])
        node.right = rnode
        newTrapezoidsBelow[0].node = rnode

    i = 0
    j = 0
    k = len(newTrapezoidsAbove)
    m = len(newTrapezoidsBelow)

    while i + j < len(trapezoids) - 2:
        node = trapezoids[i + j + 1].node
        node.type = 'snode'
        node.label = segment

        if newTrapezoidsAbove[i].rightPoint > newTrapezoidsBelow[j].rightPoint or i == k - 1:
            j += 1
            lnode = newTrapezoidsAbove[i].node
            node.left = lnode
            rnode = DNode('tnode', newTrapezoidsBelow[j])
            node.right = rnode
            newTrapezoidsBelow[j].node = rnode
        else:
            i += 1
            lnode = DNode('tnode', newTrapezoidsAbove[i])
            node.left = lnode
            newTrapezoidsAbove[i].node = lnode
            rnode = newTrapezoidsBelow[j].node
            node.right = rnode

    node = trapezoids[-1].node
    if right:
        node.type = 'pnode'
        node.label = segment.right
        rnode = DNode('tnode', right)
        node.right = rnode
        right.node = rnode
        lnode = DNode('snode', segment)
        node.left = lnode
        lastNode = lnode
    else:
        node.type = 'snode'
        node.label = segment
        lastNode = node

    if i == k - 1 and j == m - 1:
        lastNode.left = newTrapezoidsAbove[i].node
        lastNode.right = newTrapezoidsBelow[j].node
    elif j == m - 1:
        lnode = DNode('tnode', newTrapezoidsAbove[-1])
        lastNode.left = lnode
        newTrapezoidsAbove[-1].node = lnode
        lastNode.right = newTrapezoidsBelow[j].node
    else:
        rnode = DNode('tnode', newTrapezoidsBelow[-1])
        lastNode.right = rnode
        newTrapezoidsBelow[-1].node = rnode
        lastNode.left = newTrapezoidsAbove[i].node


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

    return x1, x2, y1, y3


def createOuter(lines):
    x1, x2, y1, y2 = bounds(lines)
    lowLeft = Point(x1, y1)
    lowRight = Point(x2, y1)
    upRight = Point(x2, y2)
    upLeft = Point(x1, y2)
    topSegment = Segment(upLeft, upRight)
    bottomSegment = Segment(lowLeft, lowRight)
    return Trapezoid(topSegment, bottomSegment, upLeft, upRight)


def generateParallelSegments(maxX, maxY, n):
    divider = maxY / 2.0
    above = n // 2
    below = n - n // 2
    segments = []

    deltaX = deltaY = (maxY - divider) / (above + 1)
    for i in range(1, above + 1):
        segments.append(((i * deltaX, divider + deltaY), (maxX - i * deltaX, divider + deltaY)))

    deltaY = divider / (below + 1)
    for i in range(1, below + 1):
        segments.append((((i - 0.5) * deltaX, divider - deltaY), (maxX - (i - 0.5) * deltaX, divider - deltaY)))

    return segments


def generateUniformPoints(maxX, maxY, n):
    x_coord = np.random.uniform(1, maxX, n)
    y_coord = np.random.uniform(1, maxY, n)

    res = [(x, y) for x, y in zip(x_coord, y_coord)]
    return res
