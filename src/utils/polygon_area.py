from typing import Sequence, Union, Tuple

from pymunk import Vec2d


def polygon_area(verts: Sequence[Union[Tuple[float, float], Vec2d]]) -> float:
    area = 0
    k = len(verts)
    for i in range(k):
        area += verts[i][1] * (verts[(i + 1) % k] - verts[(i - 1) % k])
    return abs(area) * 0.5
