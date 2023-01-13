from abc import ABC
from typing import Dict, Optional

from pygame import Surface
from pymunk import Vec2d

from src.entities.gadgets.drills.drill import Drill
from src.entities.gadgets.weapon.abstract_weapon import AbstractStateWeapon
from src.entities.modifiers_and_characteristics import (
    MiningCharacteristics,
    HealthLifeCharacteristics,
    VelocityCharacteristics,
    WeaponModifiers,
)
from src.entities.pilots.abstract import Pilot
from src.entities.spaceships.miner.abstract_miner import AbstractMiner


class MinerMixin(AbstractMiner, ABC):

    drill: Drill

    def __init__(
        self,
        pos: Vec2d,
        weapon_modifiers: Optional[WeaponModifiers] = None,
        velocity_characteristics: Optional[VelocityCharacteristics] = None,
        life_characteristics: Optional[HealthLifeCharacteristics] = None,
        mining_characteristics: Optional[MiningCharacteristics] = None,
        mass: Optional[float] = None,
        moment: Optional[float] = None,
        weapon: Optional[AbstractStateWeapon] = None,
        entity_id: Optional[int] = None,
        pilot: Optional[Pilot] = None,
    ):
        super().__init__(
            pos=pos,
            weapon_modifiers=weapon_modifiers,
            velocity_characteristics=velocity_characteristics,
            life_characteristics=life_characteristics,
            mass=mass,
            moment=moment,
            weapon=weapon,
            entity_id=entity_id,
            pilot=pilot,
        )
        if mining_characteristics is None:
            mining_characteristics = MiningCharacteristics.from_dict(
                self.start_config["mining_characteristics"]
            )
        self.mining_characteristics = mining_characteristics
        self.drill = Drill(self.id)

    def render(self, screen: Surface, camera) -> None:
        self.drill.render(screen, camera)
        super().render(screen, camera)

    def update(self, dt) -> None:
        super().update(dt)
        self.drill.update(dt)

    @staticmethod
    def get_characteristics(data: Dict) -> Dict:
        return {
            **AbstractMiner.get_characteristics(data),
            "mining_characteristics": MiningCharacteristics.from_dict(
                data["mining_characteristics"]
            ),
        }

    def characteristics_to_dict(self) -> Dict:
        return {
            **super().characteristics_to_dict(),
            "mining_characteristics": self.mining_characteristics.to_dict(),
        }
