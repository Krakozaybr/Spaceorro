from abc import ABC

from src.entities.abstract.abstract import Entity
from src.entities.modifiers_and_characteristics import HealthLifeCharacteristics


class HealthEntityMixin(Entity, ABC):
    life_characteristics: HealthLifeCharacteristics
