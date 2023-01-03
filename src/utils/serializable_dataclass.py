from typing import Dict, List, Optional, Type, Callable

from src.abstract import Serializable
from src.utils.all_annotations import all_annotations


class SerializableDataclass(Serializable):

    fields: Optional[List[str]]
    special_fields_serializing: Optional[Dict[str, Callable]]
    special_fields_deserializing: Optional[Dict[str, Callable]]

    def to_dict(self) -> Dict:
        res = dict()
        sfs = getattr(self, "special_fields_serializing", dict())
        for field_name in self.get_fields():
            val = getattr(self, field_name)
            if isinstance(val, Serializable):
                res[field_name] = val.to_dict()
            elif field_name in sfs:
                res[field_name] = sfs[field_name](val)
            else:
                res[field_name] = val
        return res

    @classmethod
    def from_dict(cls, data: Dict):
        vals = dict()
        sfd = getattr(cls, "special_fields_deserializing", dict())
        for field_name, field_cls in all_annotations(cls).items():
            if field_name in SerializableDataclass.__annotations__:
                continue
            if isinstance(field_cls, type(Serializable)):
                field_cls: Type[Serializable]
                vals[field_name] = field_cls.from_dict(data[field_name])
            elif field_name in sfd:
                vals[field_name] = sfd[field_name](data[field_name])
            else:
                vals[field_name] = data[field_name]
        return cls(**vals)

    def get_fields(self):
        if not hasattr(self, "fields"):
            return self.__dict__.keys()
        return self.fields
