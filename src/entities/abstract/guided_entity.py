from abc import ABC

from src.entities.abstract.abstract import Entity, Pilot, entities
from src.entities.modifiers_and_characteristics import (
    WeaponModifiers,
    VelocityCharacteristics,
)
from src.entities.gadgets.engines.abstract import Engine
from src.entities.gadgets.weapon.abstract_weapon import AbstractStateWeapon


class GuidedEntity(Entity, ABC):
    pilot: Pilot
    weapon: AbstractStateWeapon
    weapon_modifiers: WeaponModifiers
    velocity_characteristics: VelocityCharacteristics
    engine: Engine
