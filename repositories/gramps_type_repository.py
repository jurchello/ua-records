from __future__ import annotations

from typing import Any, List, Mapping, Sequence
from gramps.gen.lib.grampstype import GrampsType
from repositories.repository_core import RepositoryCore


class GrampsTypeRepository(RepositoryCore):
    POS_STRING = 1
    POS_VALUE = 0
    _CUSTOM = GrampsType._CUSTOM
    _DEFAULT = GrampsType._DEFAULT

    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_custom(self, obj) -> int:
        return obj.get_custom()

    def get_map(self, obj) -> Mapping[Any, Any]:
        return obj.get_map()

    def get_menu(self, obj) -> Sequence[Sequence[Any]]:
        return obj.get_menu()

    def get_menu_standard_xml(self, obj) -> Sequence[Sequence[Any]]:
        return obj.get_menu_standard_xml()

    @classmethod
    def get_schema(cls) -> dict:
        return GrampsType.get_schema()

    def get_standard_names(self, obj) -> List[str]:
        return obj.get_standard_names()

    def get_standard_xml(self, obj) -> List[str]:
        return obj.get_standard_xml()

    def is_custom(self, obj) -> bool:
        return obj.is_custom()

    def is_default(self, obj) -> bool:
        return obj.is_default()

    def serialize(self, obj) -> Any:
        return obj.serialize()

    def set(self, obj, value: Any) -> None:
        obj.set(value)

    def set_from_xml_str(self, obj, value: str) -> None:
        obj.set_from_xml_str(value)

    def unserialize(self, obj, data: Any) -> None:
        obj.unserialize(data)

    def xml_str(self, obj) -> str:
        return obj.xml_str()

    def value(self, obj) -> int:
        try:
            return obj.value
        except AttributeError:
            return obj.serialize()[self.POS_VALUE]

    def string(self, obj) -> str:
        try:
            return obj.string
        except AttributeError:
            return obj.serialize()[self.POS_STRING]
