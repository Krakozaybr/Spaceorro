from typing import List, Dict

from src.map.abstract import AbstractCluster, AbstractMap, AbstractMapGenerator, AbstractClustersStore
import json
from src.entities.abstract import Entity
from src.map.settings import CLUSTER_SIZE


class Cluster(AbstractCluster):

    def __init__(self):
        self.entities = []

    def update(self, dt):
        for entity in self.entities:
            entity.update(dt)

    def render(self, screen, camera):
        for entity in self.entities:
            entity.render(screen, camera)

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def remove_entity(self, entity: Entity):
        self.entities.remove(entity)

    def extra_entities(self, cluster_x, cluster_y):
        result = []
        w, h = CLUSTER_SIZE
        min_x, max_x = w * cluster_x, (cluster_x + 1) * w
        min_y, max_y = h * cluster_y, (cluster_y + 1) * h
        for entity in self.entities:
            x, y = entity.pos.x, entity.pos.y
            if not (min_x <= x < max_x and min_y <= y < max_y):
                result.append(entity)
        return result

    def serialize(self) -> str:
        return json.dumps([entity.serialize() for entity in self.entities])

    @staticmethod
    def deserialize(data: str):
        cluster = Cluster()
        cluster.entities = json.loads(data)
        return cluster


class ClustersStore(AbstractClustersStore):
    lines: Dict[int, Dict[int, Cluster]]

    def __init__(self):
        self.lines = dict()

    def __getitem__(self, item):
        x, y = item
        if isinstance(x, int) and isinstance(y, int):
            if y in self.lines:
                return self.lines[y].get(x, None)
            return None
        raise TypeError

    def __setitem__(self, key, value):
        x, y = key
        if isinstance(x, int) and isinstance(y, int) and isinstance(value, Cluster):
            self.lines[y][x] = value
        raise TypeError

    def keys(self):
        return [(x, y) for y, val in self.lines.items() for x in val.keys()]

    def values(self):
        return [cluster for line in self.lines.values() for cluster in line.values()]

    def serialize(self) -> str:
        return json.dumps({
            'class_name': self.__class__.__name__,
            'lines': {
                y: {
                    x: cluster.serialize() for x, cluster in line.items()
                } for y, line in self.lines.items()
            }
        })

    @staticmethod
    def deserialize(data: str):
        deserialized = json.loads(data)
        store = ClustersStore()
        store.lines = {
            y: {
                x: Cluster.deserialize(ser_cluster) for x, ser_cluster in line.items()
            } for y, line in deserialized['lines']
        }
        return store


class BasicMapGenerator(AbstractMapGenerator):
    # TODO make generation more complex
    def generate_clusters(self, x, y, clusters) -> List[AbstractCluster]:
        return [Cluster()]


class BasicMap(AbstractMap):
    def __init__(self):
        self.clusters = ClustersStore()
        self.map_generator = BasicMapGenerator()

    @staticmethod
    def define_pos(entity: Entity):
        w, h = CLUSTER_SIZE
        return entity.pos.x // w, entity.pos.y // h

    # TODO
    def render_at(self, x, y):
        pass

    # TODO
    def update_at(self, x, y):
        pass

    def serialize(self) -> str:
        return json.dumps({
            'class_name': self.__class__.__name__,
            'clusters': self.clusters.serialize()
        })

    @staticmethod
    def deserialize(data: str):
        deserialized = json.loads(data)
        basic_map = BasicMap()
        basic_map.clusters = ClustersStore.deserialize(deserialized['clusters'])
        return basic_map
