from typing import Tuple, Sequence, Union, List

from pymunk import Vec2d


# Applies rotation for vertices
def apply_rotation_for_verts(
    vertices: Union[Sequence[Vec2d], Sequence[Tuple[float, float]]],
    angle: float,
    pos=Vec2d.zero(),
) -> List[Tuple[float, float]]:
    if not isinstance(vertices[0], Vec2d):
        vertices = [Vec2d(*i) for i in vertices]
    result = []
    for v in vertices:
        x = v.rotated(angle)[0]
        y = v.rotated(angle)[1]
        result.append((x + pos.x, y + pos.y))
    return result
