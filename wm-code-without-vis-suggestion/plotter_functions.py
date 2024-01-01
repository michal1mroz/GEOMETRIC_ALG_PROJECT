import numpy as np
from vis_bit.main import Visualizer
from DataStructures import *
from util import *


def trapezoidal_map_vis(segments):
    S = []
    scenes = []
    for i in permute(segments):
        p1 = Point(i[0][0], i[0][1])
        p2 = Point(i[1][0], i[1][1])
        S.append(Segment(p1, p2))

    R = createOuter(segments)
    rootNode = DNode('tnode', R)
    T = DTree(rootNode)

    vis = draw_map(T, R)
    scenes.append(vis)
    for segment in S:
        intersectedTrapezoids = followSegment(T, segment)
        print(intersectedTrapezoids[0])
        if len(intersectedTrapezoids) == 1:
            insertIntoOne(T, intersectedTrapezoids[0], segment)
        else:
            insertIntoMany(T, intersectedTrapezoids, segment)

        vis = draw_map(T, R)
        scenes.append(vis)

    return T, scenes


def draw_map(D,R):
    vis = Visualizer()
    trapezoids = []
    find_all_trapezoids(D.root, trapezoids)
    for trapezoid in trapezoids:
        vis = draw_trapezoid(trapezoid, vis)
    vis = draw_grid(R, vis)
    return vis


def find_all_trapezoids(node, trapezoids):
    if node.type == 'tnode':
        trapezoids.append(node.label)
    else:
        find_all_trapezoids(node.left, trapezoids)
        find_all_trapezoids(node.right, trapezoids)


def draw_grid(R: Trapezoid, vis):
    vis.add_line_segment((R.topSegment.toTuple(), R.bottomSegment.toTuple()), color="brown")
    R_left = Segment(R.bottomSegment.left, Point(R.leftPoint.x, R.rightPoint.y))
    R_right = Segment(Point(R.rightPoint.x, R.leftPoint.y), R.bottomSegment.right)
    vis.add_line_segment((R_left.toTuple(), R_right.toTuple()), color="brown")
    return vis


def draw_trapezoid(trapezoid: Trapezoid,vis,color="green"):

    vis.add_point((trapezoid.leftPoint.toTuple(), trapezoid.rightPoint.toTuple()), color="blue")
    upper = trapezoid.topSegment.toTuple()
    lower = trapezoid.bottomSegment.toTuple()
    left_x=trapezoid.leftPoint.x
    Segment.updateX(left_x)

    #left_lower=trapezoid.bottomSegment.at_x()
    #left_upper=trapezoid.upper.at_x()
    #left_vertical=(section_to_tuple(Section(left_lower,left_upper)))
    #right_x=trapezoid.right_p.x
    #Section.update_x(right_x)
    #right_lower=trapezoid.lower.at_x()
    #right_upper=trapezoid.upper.at_x()
    #right_vertical=(section_to_tuple(Section(right_lower,right_upper)))
    #vis.add_line_segment((upper,lower,left_vertical,right_vertical),color=color)
    return vis


def insertIntoOne(T: DTree, trapezoid: Trapezoid, segment: Segment):
    p, q = segment.left, segment.right
    bottomLeft = trapezoid.bottomLeft
    bottomRight = trapezoid.bottomRight
    topLeft = trapezoid.topLeft
    topRight = trapezoid.topRight

    left, right = None, None
    top = Trapezoid(trapezoid.topSegment, segment, p, q) # C
    bottom = Trapezoid(segment, trapezoid.bottomSegment, p, q) # D

    if trapezoid.leftPoint < p:
        left = Trapezoid(trapezoid.topSegment, trapezoid.bottomSegment, trapezoid.leftPoint, p)
        left.bottomLeft = bottomLeft
        left.topLeft = topLeft
        left.topRight = top
        left.bottomRight = bottom
        top.topLeft = left
        bottom.bottomLeft = left
        updateLeft(trapezoid, left)
    else:
        Segment.updateX(p.x)
        bottom.bottomLeft = bottomLeft
        top.topLeft = topLeft
        if bottomLeft:
            bottomLeft.bottomRight = bottom
            if bottomLeft.topSegment > segment:
                bottomLeft.topRight = top
                top.bottomLeft = bottomLeft
        if topLeft:
            topLeft.topRight = top
            if segment > topLeft.bottomSegment:
                topLeft.bottomRight = bottom
                bottom.topLeft = topLeft

    if trapezoid.rightPoint > q:
        right = Trapezoid(trapezoid.topSegment, trapezoid.bottomSegment, segment.right, trapezoid.rightPoint)
        right.bottomRight = bottomRight
        right.topRight = topRight
        right.bottomLeft = bottom
        right.topLeft = top
        top.topRight = right
        bottom.bottomRight = right
        updateRight(trapezoid, right)
    else:
        Segment.updateX(q.x)
        bottom.bottomRight = bottomRight
        top.topRight = topRight
        if bottomRight:
            bottomRight.bottomLeft = bottom
            if bottomRight.topSegment > segment:
                bottomRight.topLeft = top
                top.bottomRight = bottomRight
        if topRight:
            topRight.topLeft = top
            if segment > topRight.bottomSegment:
                topRight.bottomLeft = bottom
                bottom.topRight = topRight
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

    #updateTreeOne(trapezoid, segment, left, top, bottom, right)


def insertIntoMany(T, trapezoids: list[Trapezoid], segment: Segment):
    p, q = segment.left, segment.right
    left, right = None, None
    newTrapezoidsAbove = []
    newTrapezoidsBelow = []
    n = len(trapezoids)
    first = trapezoids[0]
    bottomLeft = first.bottomLeft
    topLeft = first.topLeft
    topRight = first.topRight
    bottomRight = first.bottomRight
    Segment.updateX(first.rightPoint.x)

    if segment.isAbove(first.rightPoint):
        top = Trapezoid(first.topSegment, segment, p, first.rightPoint)
        bottom = Trapezoid(segment, first.bottomSegment, p, Point(Segment.x, segment.getY(Segment.x)))
        merge = "lower"
    else:
        top = Trapezoid(first.topSegment, segment, p, Point(Segment.x, segment.getY(Segment.x)))
        bottom = Trapezoid(segment, first.bottomSegment, p, first.rightPoint)
        merge = "upper"

    if first.leftPoint < p:
        left = Trapezoid(first.topSegment, first.bottomSegment, first.leftPoint, p)
        left.bottomLeft = bottomLeft
        left.topLeft = topLeft
        left.topRight = top
        left.bottomRight = bottom
        top.topLeft = left
        bottom.bottomLeft = left
        updateLeft(first, left)
    else:
        bottom.bottomLeft = bottomLeft
        top.topLeft = topLeft
        if bottomLeft:
            bottomLeft.bottomRight = bottom
            if bottomLeft.topSegment > segment:
                bottomLeft.topRight = top
                top.bottomLeft = bottomLeft
        if topLeft:
            topLeft.topRight = top
            if segment > topLeft.bottomSegment:
                topLeft.bottomRight = bottom
                bottom.topLeft = topLeft

    if trapezoids[1] == first.bottomRight:
        top.topRight = topRight
        if topRight:
            topRight.topLeft = top
    else:
        bottom.bottomRight = bottomRight
        if bottomRight:
            bottomRight.bottomLeft = bottom

    newTrapezoidsAbove.append(top)
    newTrapezoidsBelow.append(bottom)

    for i in range(1, n - 1):
        nextPoint = trapezoids[i].rightPoint
        bottomLeft = trapezoids[i].bottomLeft
        topLeft = trapezoids[i].topLeft
        topRight = trapezoids[i].topRight
        bottomRight = trapezoids[i].bottomRight
        Segment.updateX(nextPoint.x)

        if segment.isAbove(nextPoint):
            lowerRightPoint = Point(Segment.x, segment.getY(Segment.x))
            if merge == "upper":
                top.rightPoint = nextPoint
                t = Trapezoid(segment, trapezoids[i].bottomSegment, bottom.rightPoint, lowerRightPoint)
                bottom.topRight = t
                t.topLeft = bottom
                t.bottomLeft = bottomLeft
                if bottomLeft:
                    bottomLeft.bottomRight = t
                top.topRight = topRight
                if topRight:
                    topRight.topLeft = top
                bottom = t
                newTrapezoidsBelow.append(bottom)
            else:
                bottom.rightPoint = lowerRightPoint
                t = Trapezoid(trapezoids[i].topSegment, segment, top.rightPoint, nextPoint)
                top.bottomRight = t
                t.bottomLeft = top
                t.topLeft = topLeft
                t.topRight = topRight
                if topLeft:
                    topLeft.topRight = t
                if topRight:
                    topRight.topLeft = t
                top = t
                newTrapezoidsAbove.append(top)
            merge = "lower"
        else:
            upperRightPoint = Point(Segment.x, segment.getY(Segment.x))
            if merge == "upper":
                top.rightPoint = upperRightPoint
                t = Trapezoid(segment, trapezoids[i].bottomSegment, bottom.rightPoint, nextPoint)
                bottom.topRight = t
                t.topLeft = bottom
                t.bottomLeft = bottomLeft
                t.bottomRight = bottomRight
                if bottomLeft:
                    bottomLeft.bottomRight = t
                if bottomRight:
                    bottomRight.bottomLeft = t
                bottom = t
                newTrapezoidsBelow.append(bottom)
            else:
                bottom.rightPoint = nextPoint
                t = Trapezoid(trapezoids[i].topSegment, segment, top.rightPoint, upperRightPoint)
                top.bottomRight = t
                t.bottomLeft = top
                t.topLeft = topLeft
                if topLeft:
                    topLeft.topRight = t
                bottom.bottomRight = bottomRight
                if bottomRight:
                    bottomRight.bottomLeft = bottom
                top = t
                newTrapezoidsAbove.append(top)
            merge = "upper"

    last = trapezoids[n - 1]
    bottomLeft = last.bottomLeft
    topLeft = last.topLeft
    topRight = last.topRight
    bottomRight = last.bottomRight
    Segment.updateX(last.rightPoint)

    if merge == "upper":
        top.rightPoint = q
        t = Trapezoid(segment, last.bottomSegment, bottom.rightPoint, q)
        bottom.topRight = t
        t.topLeft = bottom
        bottom = t
        newTrapezoidsBelow.append(bottom)
    else:
        bottom.rightPoint = q
        t = Trapezoid(last.topSegment, segment, top.rightPoint, q)
        top.bottomRight = t
        t.bottomLeft = top
        top = t
        newTrapezoidsAbove.append(top)

    if last.rightPoint > q:
        right = Trapezoid(last.topSegment, last.bottomSegment, q, last.rightPoint)
        right.bottomLeft = bottom
        right.topLeft = top
        right.topRight = topRight
        right.bottomRight = bottomRight
        top.topRight = right
        bottom.bottomRight = right
        updateRight(last, right)
    else:
        top.topRight = topRight
        bottom.bottomRight = bottomRight
        if bottomRight:
            bottomRight.bottomLeft = bottom
            if bottomRight.topSegment > segment:
                bottomRight.topLeft = top
                top.bottomRight = bottomRight
        if topRight:
            topRight.topLeft = top
            if segment > topRight.bottomSegment:
                topRight.bottomLeft = bottom
                bottom.topRight = topRight

    if last == trapezoids[n - 2].topRight:
        bottom.bottomLeft = bottomLeft
        if bottomLeft:
            bottomLeft.bottomRight = bottom
    else:
        top.topLeft = topLeft
        if topLeft:
            topLeft.topRight = top
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

    #updateTreeMany(trapezoids, segment, newTrapezoidsAbove, newTrapezoidsBelow, left, right)