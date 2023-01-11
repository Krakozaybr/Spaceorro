from typing import Tuple, List, Union

from pymunk import Vec2d


# Source: https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/


class Line:
    def __init__(self, p1: Vec2d, p2: Vec2d):
        self.p1 = p1
        self.p2 = p2


def on_line(l1, p):
    # Check whether p is on the line or not
    if (
        p.x <= max(l1.p1.x, l1.p2.x)
        and p.x <= min(l1.p1.x, l1.p2.x)
        and (p.y <= max(l1.p1.y, l1.p2.y) and p.y <= min(l1.p1.y, l1.p2.y))
    ):
        return True
    return False


def direction(a, b, c):
    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if val == 0:
        # Colinear
        return 0
    elif val < 0:
        # Anti-clockwise direction
        return 2
    # Clockwise direction
    return 1


def is_intersect(l1, l2):
    # Four direction for two lines and points of other line
    dir1 = direction(l1.p1, l1.p2, l2.p1)
    dir2 = direction(l1.p1, l1.p2, l2.p2)
    dir3 = direction(l2.p1, l2.p2, l1.p1)
    dir4 = direction(l2.p1, l2.p2, l1.p2)

    # When intersecting
    if dir1 != dir2 and dir3 != dir4:
        return True

    # When p2 of line2 are on the line1
    if dir1 == 0 and on_line(l1, l2.p1):
        return True

    # When p1 of line2 are on the line1
    if dir2 == 0 and on_line(l1, l2.p2):
        return True

    # When p2 of line1 are on the line2
    if dir3 == 0 and on_line(l2, l1.p1):
        return True

    # When p1 of line1 are on the line2
    if dir4 == 0 and on_line(l2, l1.p2):
        return True

    return False


def check_inside(poly: Union[List[Tuple[float, float]], List[Vec2d]], p: Vec2d):
    # When polygon has less than 3 edge, it is not polygon
    n = len(poly)
    if n < 3:
        return False

    if isinstance(poly[0], list):
        poly = [Vec2d(*i) for i in poly]

    # Create a point at infinity, y is same as point p
    exline = Line(p, Vec2d(9999, p.y))
    count = 0
    i = 0
    while True:
        # Forming a line from two consecutive points of poly
        side = Line(poly[i], poly[(i + 1) % n])
        if is_intersect(side, exline):
            # If side is intersects ex
            if direction(side.p1, p, side.p2) == 0:
                return on_line(side, p)
            count += 1

        i = (i + 1) % n
        if i == 0:
            break

    # When count is odd
    return count & 1
