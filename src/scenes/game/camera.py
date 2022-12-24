from typing import Union
from src.utils.vector import Vector
from src.entities.abstract import Entity


# TODO maybe there is more convenient implementation
class Camera:
    def __init__(self):
        self.dv = Vector(0, 0)

    def look_at(self, entity_or_x: Union[Entity, int], y: int = None):
        if isinstance(entity_or_x, Entity):
            self.dv = entity_or_x.pos
        elif isinstance(entity_or_x, Vector):
            self.dv = entity_or_x
        else:
            assert isinstance(entity_or_x, int)
            assert isinstance(y, int)
            self.dv = Vector(entity_or_x, y)
