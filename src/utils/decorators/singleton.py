from typing import Type


def singleton(cls):
    instances = {}

    def getinstance() -> cls:
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


def generic_singleton(cls):
    instances = {}

    def get_instance(generic: Type):
        if (cls, generic) not in instances:
            instances[(cls, generic)] = cls[generic]()
        return instances[(cls, generic)]

    class Singleton:
        def __getitem__(self, item: Type):
            return lambda: get_instance(item)

        def __call__(self) -> cls:
            return get_instance(object)

    return Singleton()
