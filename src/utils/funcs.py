import math

from pymunk import Vec2d


def distance_from_rect_to_point(
    rect_pos: Vec2d, rect_width: float, rect_height: float, point: Vec2d
):
    rx, ry = rect_pos
    px, py = point
    cx = max(min(px, rx + rect_width), rx)
    cy = max(min(ry + rect_height, py), ry)
    return math.sqrt((px - cx) ** 2 + (py - cy) ** 2)


def rects_overlapped_by_circle(
    rect_w: float, rect_h: float, circle_pos: Vec2d, circle_r: float
):
    rects = []
    cx, cy = circle_pos
    min_x = int((cx - circle_r) // rect_w)
    max_x = int((cx + circle_r) // rect_w)
    min_y = int((cy - circle_r) // rect_h)
    max_y = int((cy + circle_r) // rect_h)

    for rx in range(min_x, max_x + 1):
        for ry in range(min_y, max_y + 1):
            if distance_from_rect_to_point(
                Vec2d(rx * rect_w, ry * rect_h),
                rect_w, rect_h, circle_pos
            ) <= circle_r:
                rects.append((rx, ry))

    return rects
