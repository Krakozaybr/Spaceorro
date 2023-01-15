from enum import Enum
from typing import Dict, Tuple, Iterable, Union, Optional

import pygame

from src.abstract import Serializable
from src.settings import RESOURCES_IMAGES, RESOURCES_COLORS
from src.utils.image_manager import ImageManager


class ResourceType(Enum):
    gold = RESOURCES_IMAGES["gold"]
    eternium = RESOURCES_IMAGES["eternium"]
    infinitum = RESOURCES_IMAGES["infinitum"]
    mithril = RESOURCES_IMAGES["mithril"]
    crystallium = RESOURCES_IMAGES["crystallium"]
    _colors: Dict["ResourceType", Tuple[int, int, int]]

    def get_image(self, w: int = None, h: int = None) -> pygame.Surface:
        return ImageManager().get_pic(self.value, w, h)

    def get_color(self):
        cls = self.__class__
        if not hasattr(cls, "_colors"):
            cls._colors = {
                ResourceType.gold: RESOURCES_COLORS["gold"],
                ResourceType.eternium: RESOURCES_COLORS["eternium"],
                ResourceType.infinitum: RESOURCES_COLORS["infinitum"],
                ResourceType.mithril: RESOURCES_COLORS["mithril"],
                ResourceType.crystallium: RESOURCES_COLORS["crystallium"],
            }
        return cls._colors.get(self, (100, 100, 100))

    @classmethod
    def from_name(cls, name: str) -> "ResourceType":
        return getattr(cls, name)

    def __str__(self):
        return self.name


class Resource(Serializable):

    _quantity: float
    _resource_type: ResourceType

    def __init__(self, quantity: float, resource_type: ResourceType):
        self._quantity = quantity
        self._resource_type = resource_type

    def __add__(self, other: Union[float, int, "Resource"]):
        if isinstance(other, int) or isinstance(other, float):
            return Resource(self.quantity + other, self.resource_type)
        elif other.resource_type == self.resource_type:
            return Resource(self.quantity + other.quantity, self.resource_type)
        raise ValueError

    def __sub__(self, other: Union[float, int, "Resource"]):
        if isinstance(other, int) or isinstance(other, float):
            return Resource(self.quantity - other, self.resource_type)
        elif other.resource_type == self.resource_type:
            return Resource(self.quantity - other.quantity, self.resource_type)
        raise ValueError

    def __iadd__(self, other: Union[float, int, "Resource"]):
        return self + other

    def __isub__(self, other: Union[float, int, "Resource"]):
        return self + other

    def __eq__(self, other):
        return (
            isinstance(other, Resource)
            and self.resource_type == other.resource_type
            and other.quantity == self.quantity
            or (isinstance(other, float) or isinstance(other, int)) and other == self.quantity
        )

    def __hash__(self):
        return hash((self.resource_type, self.quantity))

    def __ge__(self, other):
        return self > other or other == self

    def __gt__(self, other: Union[int, float, "Resource"]):
        if isinstance(other, int) or isinstance(other, float):
            return self.quantity > other
        elif other.resource_type == self.resource_type:
            return self.quantity > other.quantity
        raise ValueError

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Resource(
                quantity=self.quantity * other, resource_type=self.resource_type
            )
        raise ValueError

    def __truediv__(self, other):
        return self * (1 / other)

    @property
    def quantity(self) -> float:
        return self._quantity

    @property
    def resource_type(self) -> ResourceType:
        return self._resource_type

    def __str__(self):
        return str(self.quantity)

    def __repr__(self):
        return str(self)

    def to_dict(self) -> Dict:
        return {"resource_type": self.resource_type.name, "quantity": self.quantity}

    def __neg__(self):
        return Resource(quantity=-self.quantity, resource_type=self.resource_type)

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            resource_type=ResourceType.from_name(data["resource_type"]),
            quantity=data["quantity"],
        )


class Resources(Serializable):
    resources: Dict[ResourceType, Resource]

    def __init__(self, resources: Optional[Dict[ResourceType, Resource]] = None):
        if resources is None:
            resources = dict()
        self.resources = resources

    def can_afford(self, resources: Union[Resource, "Resources"]):
        if isinstance(resources, Resource):
            return self.resources[resources.resource_type] >= resources
        elif isinstance(resources, Resources):
            return all(self[rt] >= val for val, rt in resources)
        raise ValueError

    def __getitem__(self, item):
        if isinstance(item, ResourceType):
            return self.resources.get(item, Resource(0, item))
        raise ValueError

    def __setitem__(self, key: ResourceType, value: Resource):
        self.resources[key] = value

    def __iter__(self) -> Iterable[Tuple[Resource, ResourceType]]:
        for rt in ResourceType:
            yield self[rt], rt

    def copy(self):
        return self.from_dict(self.to_dict())

    def to_dict(self) -> Dict:
        return {
            "resources": {str(rt): val.to_dict() for val, rt in self},
            **super().to_dict(),
        }

    @staticmethod
    def _add_to(resources: "Resources", other: Union["Resources", Resource]):
        if isinstance(other, Resources):
            for val, rt in other:
                resources[rt] = resources[rt] + val
        elif isinstance(other, Resource):
            if other.resource_type in resources.resources:
                resources.resources[other.resource_type] += other.quantity
            else:
                resources.resources[other.resource_type] = other
        else:
            raise ValueError
        return resources

    def __neg__(self):
        return Resources({rt: -val for val, rt in self})

    def __add__(self, other: Union["Resources", Resource]):
        return self._add_to(self.copy(), other)

    def __iadd__(self, other: Union["Resources", Resource]):
        return self._add_to(self, other)

    def __isub__(self, other: Union["Resources", Resource]):
        return self._add_to(self, -other)

    def __sub__(self, other: Union["Resources", Resource]):
        return self._add_to(self.copy(), -other)

    def __mul__(self, other: float):
        res = Resources()
        for resource, _ in self:
            res += resource * other
        return res

    @classmethod
    def from_dict(cls, data: Dict):
        return Resources(
            {
                ResourceType.from_name(rt): Resource.from_dict(val)
                for rt, val in data["resources"].items()
            }
        )

    def __copy__(self):
        return Resources(self.resources.copy())

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return str(self)
