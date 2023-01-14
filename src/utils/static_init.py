from abc import abstractmethod, ABC


class StaticInitMixin(ABC):
    @classmethod
    @abstractmethod
    def static_init(cls):
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        cls.static_init()
