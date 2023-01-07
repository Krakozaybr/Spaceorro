from abc import ABC, abstractmethod
from typing import Optional

from pygame.sprite import AbstractGroup
from pymunk import Vec2d

from src.abstract import Updateable
from src.entities.abstract.abstract import Entity
from src.entities.basic_entity.basic_entity import BasicEntity
from src.entities.basic_entity.view import BasicView
from src.entities.modifiers_and_characteristics import LifeCharacteristics
from src.utils.image_manager import ImageManager


class ExplosiveView(BasicView, Updateable, ABC):
    def __init__(
        self,
        entity: Entity,
        explosion_radius: float,
        fps: Optional[int] = 10,
        *groups: AbstractGroup
    ):
        super().__init__(entity, *groups)
        # exploding params
        self.started_exposing = False
        self.animation_in_process = False
        self.cur_image = 0
        self.time = 0
        self.fps = fps
        self.explosion_radius = explosion_radius

    def start_exploding(self):
        self.started_exposing = True
        self.animation_in_process = True
        self.update_explosion_image()

    def update(self, dt: float):
        if self.animation_in_process:
            explosion_frames = ImageManager().explosion_frames()
            self.time += dt
            self.cur_image = int(self.time // (1 / self.fps))
            if self.cur_image >= len(explosion_frames):
                self.animation_in_process = False
            else:
                self.update_explosion_image()

    def update_explosion_image(self):
        self.image = ImageManager().explosion_frames(
            int(self.explosion_radius * 2), int(self.explosion_radius * 2)
        )[self.cur_image]

    @property
    def animation_passed(self):
        return self.started_exposing and not self.animation_in_process


class Explosive(BasicEntity, ABC):
    view: ExplosiveView
    exploding: bool

    def __init__(
        self,
        pos: Vec2d,
        life_characteristics: Optional[LifeCharacteristics] = None,
        mass: Optional[float] = None,
        moment: Optional[float] = None,
        entity_id: Optional[int] = None,
    ):
        super().__init__(
            pos=pos,
            life_characteristics=life_characteristics,
            mass=mass,
            moment=moment,
            entity_id=entity_id,
        )
        self.exploding = False

    @abstractmethod
    def on_explode(self):
        pass

    def update(self, dt: float):
        super().update(dt)
        self.view.update(dt)
        if not self.exploding and not self.is_alive:
            self.explode()
        if self.exploding and self.view.animation_passed:
            self.is_active = False

    def explode(self):
        self.control_body.velocity = Vec2d.zero()
        self.die()
        self.exploding = True
        self.view.start_exploding()
        self.on_explode()
