from abc import ABC

from src.entities.abstract.abstract import Entity, Pilot
from src.entities.gadgets.engines.abstract import Engine
from src.entities.gadgets.weapon.abstract_weapon import AbstractStateWeapon
from src.entities.modifiers_and_characteristics import (
    WeaponModifiers,
    VelocityCharacteristics,
)


class AbstractSpaceship(Entity, ABC):
    pilot: Pilot
    weapon: AbstractStateWeapon
    weapon_modifiers: WeaponModifiers
    velocity_characteristics: VelocityCharacteristics
    engine: Engine
