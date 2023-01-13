from abc import ABC

from src.entities.basic_entity.basic_spaceship import (
    BasicSpaceship,
)
from src.entities.modifiers_and_characteristics import (
    MiningCharacteristics,
)


class AbstractMiner(BasicSpaceship, ABC):

    mining_characteristics: MiningCharacteristics
