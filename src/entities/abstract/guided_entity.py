from abc import ABC, abstractmethod

from src.entities.abstract.abstract import Entity
from src.entities.pilots.abstract import Pilot
from src.entities.gadgets.engines.abstract import Engine
from src.entities.gadgets.weapon.abstract_weapon import AbstractStateWeapon
from src.entities.modifiers_and_characteristics import (
    WeaponModifiers,
    VelocityCharacteristics,
)
from src.entities.teams import Team


class AbstractSpaceship(Entity, ABC):
    pilot: Pilot
    weapon: AbstractStateWeapon
    weapon_modifiers: WeaponModifiers
    velocity_characteristics: VelocityCharacteristics
    engine: Engine

    @property
    def team(self) -> Team:
        return self.pilot.team
