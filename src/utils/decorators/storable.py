from src.utils.store import Store


def storable(cls):
    cls.store = Store[cls]()
    return cls
