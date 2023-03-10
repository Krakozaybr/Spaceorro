from enum import Enum
from typing import Optional

import pygame
import pymunk
from pygame import Surface
from pymunk import Vec2d

from src.abstract import RenderUpdateObject
from src.entities.entity_configs import AbstractEntityConfig
from src.entities.modifiers_and_characteristics import *
from src.utils.decorators import storable
from src.utils.signal import SignalAnnotationMixin, Signal
from src.utils.store import Store

ENTITY_COLLISION = 1


class SaveStrategy(Enum):
    ENTITY = 1
    DEPENDED = 2
    NOT_SAVE = 3


class StoreMixin(ABC):
    store: Store
    _obj_id: int

    def __init__(self, _obj_id: Optional[int] = None):
        assert hasattr(self, "store")
        if _obj_id is not None:
            self.obj_id = _obj_id
        else:
            self._obj_id = self.store.put_and_get_id(self)

    @classmethod
    def create_store(cls):
        return Store[cls]()

    @property
    def obj_id(self) -> int:
        return self._obj_id

    @obj_id.setter
    def obj_id(self, val: int):
        if hasattr(self, "_obj_id"):
            del self.store[self._obj_id]
        self.store[val] = self
        self._obj_id = val


class IsActiveMixin(StoreMixin, SignalAnnotationMixin, ABC):
    _is_active: bool

    on_inactive: Signal
    on_active: Signal

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, val: bool) -> None:
        self._is_active = val
        if not self.is_active:
            del self.store[self.obj_id]
            self.on_inactive.emit()
        else:
            self.store[self.obj_id] = self
            self.on_active.emit()


class EntityView(pygame.sprite.Sprite, ABC):
    @abstractmethod
    def draw(self, screen: Surface, pos: Vec2d) -> None:
        pass


@storable
class Entity(
    Serializable,
    RenderUpdateObject,
    IsActiveMixin,
    pymunk.Body,
    SignalAnnotationMixin,
    ABC,
):

    view: EntityView
    shape: pymunk.Shape
    control_body: pymunk.Body
    pivot: pymunk.PivotJoint
    life_characteristics: LifeCharacteristics
    config: AbstractEntityConfig
    is_alive: bool
    in_space: bool
    save_strategy: SaveStrategy

    on_damage: Signal

    def __init__(
        self, mass: float, moment: float, body_type: int, _obj_id: Optional[int] = None
    ):
        SignalAnnotationMixin.__init__(self)
        pymunk.Body.__init__(self, mass, moment, body_type)
        IsActiveMixin.__init__(self, _obj_id=_obj_id)
        self.__is_active = False

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        if not isinstance(cls, type(ABC)):
            assert hasattr(cls, "save_strategy")

    @abstractmethod
    def add_to_space(self, space: pymunk.Space) -> None:
        self.in_space = True

    @abstractmethod
    def remove_from_space(self, space: pymunk.Space) -> None:
        self.in_space = False

    @abstractmethod
    def take_damage(self, damage: float, sender: "Entity") -> None:
        self.on_damage.emit(damage, sender)

    def __repr__(self):
        return f"{self.__class__.__name__}(obj_id={self.obj_id})"

    @abstractmethod
    def collide(self, other):
        pass


class EntityFactory(ABC):
    @classmethod
    @abstractmethod
    def create_entity(cls, pos: Vec2d) -> Entity:
        pass
