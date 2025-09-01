from __future__ import annotations
from typing import Any, List
from gramps.gen.lib.surname import Surname
from gramps.gen.lib.nameorigintype import NameOriginType
from repositories.secondary_object_repository import SecondaryObjectRepository

class SurnameRepository(SecondaryObjectRepository):
    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_connector(self, obj: Surname) -> str:
        return obj.get_connector()

    def get_origintype(self, obj: Surname) -> NameOriginType:
        return obj.get_origintype()

    def get_prefix(self, obj: Surname) -> str:
        return obj.get_prefix()

    def get_primary(self, obj: Surname) -> bool:
        return obj.get_primary()

    @classmethod
    def get_schema(cls) -> dict:
        return Surname.get_schema()

    def get_surname(self, obj: Surname) -> str:
        return obj.get_surname()

    def get_text_data_list(self, obj: Surname) -> List[Any]:
        return obj.get_text_data_list()

    def is_empty(self, obj: Surname) -> bool:
        return obj.is_empty()

    def is_equivalent(self, obj: Surname, other: Surname) -> int:
        return obj.is_equivalent(other)

    def merge(self, obj: Surname, acquisition: Surname) -> None:
        obj.merge(acquisition)

    def serialize(self, obj: Surname) -> Any:
        return obj.serialize()

    def set_connector(self, obj: Surname, connector: str) -> None:
        obj.set_connector(connector)

    def set_origintype(self, obj: Surname, the_type: NameOriginType) -> None:
        obj.set_origintype(the_type)

    def set_prefix(self, obj: Surname, val: str) -> None:
        obj.set_prefix(val)

    def set_primary(self, obj: Surname, primary: bool = True) -> None:
        obj.set_primary(primary)

    def set_surname(self, obj: Surname, val: str) -> None:
        obj.set_surname(val)

    def unserialize(self, obj: Surname, data: Any) -> None:
        obj.unserialize(data)
