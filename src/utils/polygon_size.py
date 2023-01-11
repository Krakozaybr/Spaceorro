from math import inf
from typing import Sequence, Tuple, Union

from pymunk import Vec2d


def get_polygon_size(
    vertices: Union[Sequence[Tuple[float, float]], Sequence[Vec2d]]
) -> Tuple[float, float]:
    assert len(vertices) > 2
    if not isinstance(vertices[0], Vec2d):
        vertices = [Vec2d(*i) for i in vertices]
    min_x = min_y = inf
    max_x = max_y = -inf
    for x, y in vertices:
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
    return max_x - min_x, max_y - min_y
