from pygame.sprite import AbstractGroup

from src.entities.abstract import EntityView, Entity

import pygame


class PlayerView(EntityView):
    def __init__(self, entity: Entity, *groups: AbstractGroup):
        super().__init__(*groups)
        self.entity = entity

    def draw(self, screen, pos):
        verts = []
        shape = self.entity.shape
        for v in shape.get_vertices():
            x = v.rotated(shape.body.angle)[0]
            y = v.rotated(shape.body.angle)[1]
            verts.append((x + pos.x, y + pos.y))
        pygame.draw.polygon(screen, "red", [(dx, dy) for dx, dy in verts])
        # x, y = self.entity.position + pos
        # dx, dy = x + self.entity.velocity.x / 10, y + self.entity.velocity.y / 10
        # pygame.draw.line(screen, 'blue', (x, y), (dx, dy))
