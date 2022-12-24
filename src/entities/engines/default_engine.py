from src.entities.abstract import Engine
from src.utils.vector import Vector


# TODO implement engine as it could influence on body of entity
class DefaultEngine(Engine):
    def __init__(self):
        self.rotation_speed = 100
        self.direct_speed = 100
        self.force = Vector(0, 0)

    def rotate(self, dt):
        ...

    @property
    def current_force(self):
        return self.force
