import random
from itertools import product
from typing import List, Dict, Set, Iterable, Tuple, Optional

import pygame.draw
import pymunk
from pygame import Surface
from pymunk import Vec2d, ShapeFilter

from src.entities.get_entity import entity_from_dict
from src.entities.abstract.abstract import Entity, ENTITY_COLLISION, SaveStrategy
from src.entities.asteroids.factory import AsteroidFactory
from src.map.abstract import (
    AbstractCluster,
    AbstractMap,
    AbstractMapGenerator,
    AbstractClustersStore,
)
from src.scenes.game.camera import Camera
from src.settings import CLUSTER_SIZE, VISION_DISTANCE, LOG_GENERATING
from src.settings import SHOW_CLUSTERS_BORDERS


class EntityAlreadyAdded(Exception):
    pass


class EntityNotFound(Exception):
    pass


class Cluster(AbstractCluster):
    dependent_entities_data: List[Dict]

    balls = [
        (
            random.randint(0, CLUSTER_SIZE[0]),
            random.randint(0, CLUSTER_SIZE[1]),
            random.randint(2, 6),
        )
        for _ in range(100)
    ]

    def __init__(
        self,
        x: int,
        y: int,
        entities: Optional[Set[Entity]] = None,
        dependent_entities_data: Optional[List[Dict]] = None,
    ):
        if entities is None:
            entities = set()
        self.entities = entities
        self.pos = self.x, self.y = x, y
        if dependent_entities_data is not None:
            self.dependent_entities_data = dependent_entities_data

    def update(self, dt: float) -> None:
        for entity in self.entities.copy():
            entity.update(dt)

    def render(self, screen: Surface, camera: Camera) -> None:
        w, h = CLUSTER_SIZE
        dx, dy = camera.dv + Vec2d(self.x * w, self.y * h)
        for x, y, r in self.balls:
            pygame.draw.circle(screen, "white", (dx + x, dy + y), r)
        if SHOW_CLUSTERS_BORDERS:
            pygame.draw.line(screen, "green", (dx, dy), (dx + w, dy))
            pygame.draw.line(screen, "green", (dx + w, dy), (dx + w, dy + h))
            pygame.draw.line(screen, "green", (dx + w, dy + h), (dx, dy + h))
            pygame.draw.line(screen, "green", (dx, dy + h), (dx, dy))
        for entity in self.entities:
            entity.render(screen, camera)

    def add_entity(self, entity: Entity) -> None:
        self.entities.add(entity)

    def remove_entity(self, entity: Entity) -> None:
        self.entities.remove(entity)

    def extra_entities(self) -> List[Tuple[Entity, int, int]]:
        result = []
        w, h = CLUSTER_SIZE
        for entity in self.entities:
            x, y = entity.position.x // w, entity.position.y // h
            if x != self.x or y != self.y:
                result.append((entity, int(x), int(y)))
        return result

    def dead_entities(self) -> Iterable[Entity]:
        return filter(lambda e: not e.is_alive and e.in_space, self.entities)

    def pop_inactive_entities(self) -> Iterable[Entity]:
        result = []
        for entity in self.entities.copy():
            if not entity.is_active:
                result.append(entity)
                self.entities.remove(entity)
        return result

    def to_dict(self) -> Dict:
        return {
            **super().to_dict(),
            "x": self.x,
            "y": self.y,
            "independent_entities": [
                entity.to_dict()
                for entity in self.entities
                if entity.is_alive and entity.save_strategy == SaveStrategy.ENTITY
            ],
            "dependent_entities": [
                entity.to_dict()
                for entity in self.entities
                if entity.is_alive and entity.save_strategy == SaveStrategy.DEPENDED
            ],
        }

    @classmethod
    def from_dict(cls, data: Dict):
        cluster = Cluster(
            data["x"],
            data["y"],
            entities={
                entity_from_dict(entity) for entity in data["independent_entities"]
            },
            dependent_entities_data=data["dependent_entities"],
        )
        return cluster

    def load_depended_entities(self):
        for entity in self.dependent_entities_data:
            self.entities.add(entity_from_dict(entity))

    def __hash__(self) -> int:
        return hash(self.pos)

    def __eq__(self, other) -> bool:
        if (
            isinstance(other, AbstractCluster)
            and self.entities == other.entities
            and self.pos == other.pos
        ):
            return True
        return False

    def __contains__(self, item) -> bool:
        if isinstance(item, Entity):
            return item in self.entities
        return False


class ClustersStore(AbstractClustersStore):
    lines: Dict[int, Dict[int, Cluster]]

    def __init__(self, generator: AbstractMapGenerator):
        self.lines = dict()
        self.generator = generator

    def __getitem__(self, item) -> Cluster:
        x, y = item
        if isinstance(x, int) and isinstance(y, int):
            if not self.exists(x, y):
                if not hasattr(self, "lol"):
                    self.lol = 12
                self.generate_at(x, y)
            return self.lines[y][x]
        raise TypeError(f"Attempt to use {type(item[0])} as key")

    def __setitem__(self, key, value) -> None:
        x, y = key
        if isinstance(x, int) and isinstance(y, int) and isinstance(value, Cluster):
            if y not in self.lines:
                self.lines[y] = dict()
            self.lines[y][x] = value
            return
        raise TypeError

    def __contains__(self, item) -> bool:
        if isinstance(item, Entity):
            cx, cy = BasicMap.determine_cluster(item.position)
            return self.exists(cx, cy) and item in self[cx, cy]
        elif isinstance(item, Cluster):
            cx, cy = item.pos
            return self.exists(cx, cy) and item == self[cx, cy]
        return False

    def generate_at(self, x: int, y: int) -> None:
        for new_cluster in self.generator.generate_clusters(x, y, self):
            cx, cy = new_cluster.pos
            self[cx, cy] = new_cluster

    def exists(self, x: int, y: int) -> bool:
        return y in self.lines and x in self.lines[y]

    def keys(self) -> List[Tuple[int, int]]:
        return [(x, y) for y, val in self.lines.items() for x in val.keys()]

    def values(self) -> List[Cluster]:
        return [cluster for line in self.lines.values() for cluster in line.values()]

    def to_dict(self) -> Dict:
        return {
            **super().to_dict(),
            "lines": {
                y: {x: cluster.to_dict() for x, cluster in line.items()}
                for y, line in self.lines.items()
            },
        }

    @classmethod
    def from_dict(cls, data: Dict):
        store = ClustersStore(BasicMapGenerator())
        store.lines = {
            int(y): {
                int(x): Cluster.from_dict(ser_cluster)
                for x, ser_cluster in line.items()
            }
            for y, line in data["lines"].items()
        }
        for cluster in store.values():
            cluster.load_depended_entities()
        return store

    def __eq__(self, other):
        if isinstance(other, AbstractClustersStore):
            if list(self.keys()) != list(other.keys()):
                return False
            if any(self[x, y] != other[x, y] for x, y in self.keys()):
                return False
            return True
        return False


class BasicMapGenerator(AbstractMapGenerator):
    # TODO make generation more complex
    def generate_clusters(
        self, x: int, y: int, clusters: ClustersStore
    ) -> List[AbstractCluster]:
        if LOG_GENERATING:
            print(f"generated at {x}, {y}")
        w, h = CLUSTER_SIZE
        entities = set()
        for _ in range(random.randint(4, 7)):
            entity_x = random.randint(w * x, w * (x + 1))
            entity_y = random.randint(h * y, h * (y + 1))
            entities.add(AsteroidFactory.create_entity(Vec2d(entity_x, entity_y)))
        return [Cluster(x, y, entities=entities)]


class BasicMap(AbstractMap):
    active_clusters: Set[Cluster]

    def __init__(self):
        self.map_generator = BasicMapGenerator()
        self.clusters = ClustersStore(self.map_generator)
        self.active_clusters = set()
        self.space = pymunk.Space()
        self.space.collision_slop = 0.05
        self.space.sleep_time_threshold = 10
        self.space.damping = 0.6
        handler = self.space.add_collision_handler(ENTITY_COLLISION, ENTITY_COLLISION)
        handler.begin = self.collision

    @staticmethod
    def collision(arbiter: pymunk.Arbiter, space: pymunk.Space, data: Dict) -> bool:
        s1, s2 = arbiter.shapes
        if isinstance(s1.body, Entity) and isinstance(s2.body, Entity):
            s1.body.collide(s2.body)
            s2.body.collide(s1.body)
        return True

    def update_active_clusters(self, clusters: Set[Cluster]) -> None:
        for cluster in self.active_clusters - clusters:
            self.delete_entities_from_space(cluster.entities)
        for cluster in clusters - self.active_clusters:
            self.add_entities_to_space(cluster.entities)
        self.active_clusters = clusters

    def add_entities_to_space(self, entities: Iterable[Entity]) -> None:
        for entity in entities:
            if not entity.in_space:
                entity.add_to_space(self.space)

    def delete_entities_from_space(self, entities: Iterable[Entity]) -> None:
        for entity in entities:
            entity.remove_from_space(self.space)

    @staticmethod
    def determine_cluster(pos: Vec2d) -> Tuple[int, int]:
        w, h = CLUSTER_SIZE
        return int(pos.x // w), int(pos.y // h)

    def get_clusters_near(self, x: int, y: int) -> Set[Cluster]:
        result = set()
        for dx, dy in product(range(-VISION_DISTANCE, VISION_DISTANCE + 1), repeat=2):
            cluster = self.clusters[x + dx, y + dy]
            result.add(cluster)
        return result

    def render_at(self, screen: Surface, camera: Camera, pos: Vec2d) -> None:
        self.update_active_clusters(
            self.get_clusters_near(*self.determine_cluster(pos))
        )
        for cluster in self.active_clusters:
            cluster.render(screen, camera)

    def update_at(self, pos: Vec2d, dt: float) -> None:
        self.update_active_clusters(
            self.get_clusters_near(*self.determine_cluster(pos))
        )
        entities_for_delete = []
        for cluster in self.active_clusters:
            for entity in cluster.dead_entities():
                entity.remove_from_space(self.space)
            for entity in cluster.pop_inactive_entities():
                if entity.in_space:
                    entity.remove_from_space(self.space)
            for entity, x, y in cluster.extra_entities():
                self.clusters[x, y].add_entity(entity)
                cluster.remove_entity(entity)
                if self.clusters[x, y] not in self.active_clusters:
                    entities_for_delete.append(entity)
        self.delete_entities_from_space(entities_for_delete)
        self.space.step(dt)
        for cluster in self.active_clusters:
            cluster.update(dt)

    def to_dict(self) -> Dict:
        return {"clusters": self.clusters.to_dict(), **super().to_dict()}

    def add_entity(self, entity: Entity) -> None:
        if entity in self.clusters:
            raise EntityAlreadyAdded
        cx, cy = self.determine_cluster(entity.position)
        self.clusters[cx, cy].add_entity(entity)
        entity.add_to_space(self.space)

    def remove_entity(self, entity: Entity) -> None:
        if entity not in self.clusters:
            raise EntityNotFound
        cx, cy = self.determine_cluster(entity.position)
        self.clusters[cx, cy].remove_entity(entity)
        if entity.in_space:
            entity.remove_from_space(self.space)

    @classmethod
    def from_dict(cls, data: Dict):
        basic_map = BasicMap()
        basic_map.clusters = ClustersStore.from_dict(data["clusters"])
        return basic_map

    def get_entities_near(self, pos: Vec2d, radius: float):
        # That realization don`t make projections on shapes of entities
        # So, I decided to use native method of pymunk.Space, but it works only with shapes
        # which are inside space. However, only some entities are included in space for optimisation
        # Maybe, I`ll make it better in far future :)
        #
        # from src.utils.funcs import rects_overlapped_by_circle
        # w, h = CLUSTER_SIZE
        # res = []
        # for x, y in rects_overlapped_by_circle(w, h, pos, radius):
        #     for entity in self.clusters[x, y].entities:
        #         if entity.position.get_distance(pos) <= radius:
        #             res.append(entity)
        # return res
        res = []
        for query_info in self.space.point_query(pos, radius, ShapeFilter()):
            res.append(query_info.shape.body)
        return res

    def get_entity_at(self, pos: Vec2d):
        res = self.space.point_query_nearest(pos, 0, ShapeFilter())
        if res is not None:
            res = res.shape.body
        return res
