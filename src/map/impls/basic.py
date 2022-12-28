from itertools import product
from typing import List, Dict, Set, Iterable

import pygame.draw
import pymunk
from pymunk import Vec2d

from src.map.abstract import (
    AbstractCluster,
    AbstractMap,
    AbstractMapGenerator,
    AbstractClustersStore,
)
import json
from src.entities.abstract import Entity
from src.map.settings import CLUSTER_SIZE, VISION_RADIUS
from src.entities import deserialize as deserialize_entity
from src.scenes.game.camera import Camera
import random


class Cluster(AbstractCluster):

    balls = [(random.randint(0, CLUSTER_SIZE[0]), random.randint(0, CLUSTER_SIZE[1]), random.randint(2, 6)) for _ in range(100)]

    def __init__(self, x, y):
        self.entities = []
        self.x, self.y = self.pos = (x, y)

    def update(self, dt):
        for entity in self.entities:
            entity.update(dt)

    def render(self, screen, camera):
        W, H = CLUSTER_SIZE
        dx, dy = camera.dv + Vec2d(self.x * W, self.y * H)
        for x, y, r in self.balls:
            pygame.draw.circle(screen, 'white', (dx + x, dy + y), r)
        pygame.draw.line(screen, 'green', (dx, dy), (dx + W, dy))
        pygame.draw.line(screen, 'green', (dx + W, dy), (dx + W, dy + H))
        pygame.draw.line(screen, 'green', (dx + W, dy + H), (dx, dy + H))
        pygame.draw.line(screen, 'green', (dx, dy + H), (dx, dy))
        for entity in self.entities:
            entity.render(screen, camera)

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def remove_entity(self, entity: Entity):
        self.entities.remove(entity)

    def extra_entities(self):
        result = []
        w, h = CLUSTER_SIZE
        for entity in self.entities:
            x, y = entity.position.x // w, entity.position.y // h
            if x != self.x or y != self.y:
                result.append((entity, x, y))
        return result

    def serialize(self) -> str:
        return json.dumps(
            {
                "class_name": Cluster.__name__,
                "x": self.x,
                "y": self.y,
                "entities": [entity.serialize() for entity in self.entities],
            }
        )

    @staticmethod
    def deserialize(data: str):
        deserialized = json.loads(data)
        cluster = Cluster(deserialized["x"], deserialized["y"])
        cluster.entities = [
            deserialize_entity(entity) for entity in deserialized["entities"]
        ]
        return cluster

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return id(self) == id(other)


class ClustersStore(AbstractClustersStore):
    lines: Dict[int, Dict[int, Cluster]]

    def __init__(self, generator: AbstractMapGenerator):
        self.lines = dict()
        self.generator = generator

    def __getitem__(self, item):
        x, y = item
        if isinstance(x, int) and isinstance(y, int):
            if not self.exists(x, y):
                self.generate_at(x, y)
            return self.lines[y][x]
        raise TypeError

    def __setitem__(self, key, value):
        x, y = key
        if isinstance(x, int) and isinstance(y, int) and isinstance(value, Cluster):
            if y not in self.lines:
                self.lines[y] = dict()
            self.lines[y][x] = value
            return
        raise TypeError

    def generate_at(self, x, y):
        for new_cluster in self.generator.generate_clusters(x, y, self):
            cx, cy = new_cluster.pos
            self[cx, cy] = new_cluster

    def exists(self, x: int, y: int):
        return y in self.lines and x in self.lines[y]

    def keys(self):
        return [(x, y) for y, val in self.lines.items() for x in val.keys()]

    def values(self):
        return [cluster for line in self.lines.values() for cluster in line.values()]

    def serialize(self) -> str:
        return json.dumps(
            {
                "class_name": self.__class__.__name__,
                "lines": {
                    y: {x: cluster.serialize() for x, cluster in line.items()}
                    for y, line in self.lines.items()
                },
            }
        )

    @staticmethod
    def deserialize(data: str):
        deserialized = json.loads(data)
        store = ClustersStore()
        store.lines = {
            y: {x: Cluster.deserialize(ser_cluster) for x, ser_cluster in line.items()}
            for y, line in deserialized["lines"]
        }
        return store


class BasicMapGenerator(AbstractMapGenerator):
    # TODO make generation more complex
    def generate_clusters(self, x, y, clusters: ClustersStore) -> List[AbstractCluster]:
        print(f'generated at {x}, {y}')
        return [Cluster(x, y)]


class BasicMap(AbstractMap):
    active_clusters: Set[Cluster]

    def __init__(self):
        self.map_generator = BasicMapGenerator()
        self.clusters = ClustersStore(self.map_generator)
        self.active_clusters = set()
        self.space = pymunk.Space()

    def update_active_clusters(self, clusters: Set[Cluster]):
        for cluster in self.active_clusters - clusters:
            self.delete_entities(cluster.entities)
        for cluster in clusters - self.active_clusters:
            self.add_entities(cluster.entities)
        self.active_clusters = clusters

    def add_entities(self, entities: Iterable[Entity]):
        for entity in entities:
            entity.add_to_space(self.space)

    def delete_entities(self, entities: Iterable[Entity]):
        for entity in entities:
            entity.remove_from_space(self.space)

    @staticmethod
    def determine_cluster(pos: Vec2d):
        w, h = CLUSTER_SIZE
        return int(pos.x // w), int(pos.y // h)

    def get_clusters_near(self, x, y):
        result = set()
        for dx, dy in product(range(-VISION_RADIUS, VISION_RADIUS + 1), repeat=2):
            cluster = self.clusters[x + dx, y + dy]
            result.add(cluster)
        return result

    # TODO
    def render_at(self, screen, camera: Camera, pos: Vec2d):
        self.update_active_clusters(
            self.get_clusters_near(*self.determine_cluster(pos))
        )
        for cluster in self.active_clusters:
            cluster.render(screen, camera)

    # TODO
    def update_at(self, pos: Vec2d, dt: float):
        self.update_active_clusters(
            self.get_clusters_near(*self.determine_cluster(pos))
        )
        for cluster in self.active_clusters:
            cluster.update(dt)
        entities_for_delete = []
        for cluster in self.active_clusters:
            for entity, x, y in cluster.extra_entities():
                self.clusters[x, y].add_entity(entity)
                cluster.remove_entity(entity)
                if self.clusters[x, y] not in self.active_clusters:
                    entities_for_delete.append(entity)
        self.delete_entities(entities_for_delete)
        self.space.step(dt)

    def serialize(self) -> str:
        return json.dumps(
            {
                "class_name": self.__class__.__name__,
                "clusters": self.clusters.serialize(),
            }
        )

    @staticmethod
    def deserialize(data: str):
        deserialized = json.loads(data)
        basic_map = BasicMap()
        basic_map.clusters = ClustersStore.deserialize(deserialized["clusters"])
        return basic_map