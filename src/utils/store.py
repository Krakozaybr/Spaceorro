from typing import Generic, Dict, TypeVar

from src.utils.decorators import generic_singleton

T = TypeVar("T")


@generic_singleton
class Store(Generic[T]):
    objects: Dict[int, T]

    def __init__(self):
        self.objects = dict()
        self.current_id = 0

    def __setitem__(self, key: int, item: T):
        self.objects[key] = item

    def put_and_get_id(self, obj: T):
        while self.current_id in self.objects:
            self.current_id += 1
        self.objects[self.current_id] = obj
        self.current_id += 1
        return self.current_id - 1

    def __getitem__(self, item: int):
        return self.objects.get(item, None)

    def remove(self, obj_id: int):
        self.objects.pop(obj_id, None)

    def __delitem__(self, key: int):
        self.remove(key)

    def __contains__(self, item: T):
        return item in self.objects.values()
