from typing import Dict, Type

from src.entities.gadgets.weapon.bullets.abstract import (
    AbstractBullet,
)
from src.entities.gadgets.weapon.bullets.blaster_charge import (
    BlasterCharge,
)

bullets_classes = [BlasterCharge]
bullets_dict = {i.__name__: i for i in bullets_classes}


def find_bullet_cls_by_name(name: str) -> Type[AbstractBullet]:
    return bullets_dict[name]
