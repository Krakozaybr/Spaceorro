import math
import random
from typing import Dict, Optional

from pymunk import Vec2d

from src.entities.asteroids.abstract import AbstractAsteroid
from src.entities.basic_entity.basic_spaceship import BasicSpaceship
from src.entities.pickupable.resource import PickupableResource
from src.entities.pilots.basic_pilot import BasicPilot
from src.entities.spaceships.miner.miner_mixin import MinerMixin
from src.entities.teams import Team
from src.environment.abstract import get_environment
from src.resources import Resource, ResourceType, Resources
from src.settings import SPACESHIP_BOT_VISION_RADIUS


class SimpleBot(BasicPilot):
    def __init__(
        self,
        entity: BasicSpaceship,
        team: Team,
        _obj_id: Optional[int] = None,
        resources: Optional[Resources] = None,
    ):
        super().__init__(entity, team, _obj_id=_obj_id, resources=resources)

        # If bot does not see anything near
        self.is_searching = False
        self.searching_direction = None
        self.launched_resources = False

    def diy(self):
        for rt in ResourceType:
            self.resources += Resource(
                quantity=self.entity.life_characteristics.max_health / 30,
                resource_type=rt,
            )
        if not self.launched_resources:
            self.launched_resources = True
            env = get_environment()
            registrator = env.get_entity_registrator()
            for resource, rt in self.resources:
                if resource.quantity > 0:
                    registrator.add_entity(
                        PickupableResource(self.entity.position, resource)
                    )

    def update(self, dt: float):
        self.entity.on_death.connect(self.diy)
        env = get_environment()
        entities_near = env.get_entities_near(
            self.entity.position, SPACESHIP_BOT_VISION_RADIUS
        )
        closest_target = None
        closest_asteroid = None
        closest_pickupable_resource = None

        for entity in entities_near:
            if (
                isinstance(entity, BasicSpaceship)
                and entity.team != self.team
                and entity is not self.entity
                and (
                    closest_target is None
                    or self.entity.position.get_distance(closest_target.position)
                    > self.entity.position.get_distance(entity.position)
                )
            ):
                closest_target = entity
            elif (
                isinstance(entity, AbstractAsteroid)
                and isinstance(self.entity, MinerMixin)
                and (
                    closest_asteroid is None
                    or self.entity.position.get_distance(closest_asteroid.position)
                    > self.entity.position.get_distance(entity.position)
                )
            ):
                closest_asteroid = entity
            elif isinstance(entity, PickupableResource) and (
                closest_pickupable_resource is None
                or self.entity.position.get_distance(
                    closest_pickupable_resource.position
                )
                > self.entity.position.get_distance(entity.position)
            ):
                closest_pickupable_resource = entity

        if closest_target is not None:
            pi2 = math.pi * 2
            self.entity.engine.keep_distance(dt, closest_target.position, 300)
            angle = (
                (closest_target.position - self.entity.position).angle + math.pi * 0.5
            ) % pi2
            self.entity.engine.rotate_to(dt, angle)
            if abs(angle - (self.entity.angle % pi2)) < math.pi / 8:
                self.entity.shoot()
        elif closest_pickupable_resource is not None:
            self.entity.engine.move_to(dt, closest_pickupable_resource.position)
        elif closest_asteroid is not None:
            self.entity.engine.keep_distance(
                dt,
                closest_asteroid.position,
                self.entity.drill.config.mining_distance / 2,
            )
            self.entity.drill.set_target(closest_asteroid)
        else:
            if not self.is_searching:
                self.is_searching = True
                self.searching_direction = Vec2d(
                    random.random(), random.random()
                ).normalized()
            self.entity.engine.apply_force(self.searching_direction, dt)
        self.entity.engine.rotate_to(dt, self.entity.velocity.angle + math.pi * 0.5)

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**super().get_default_params(data))
