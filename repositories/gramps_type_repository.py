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

    def get_custom(self, obj: GrampsType) -> int:
        return obj.get_custom()

    def get_map(self, obj: GrampsType) -> Mapping[Any, Any]:
        return obj.get_map()

    def get_menu(self, obj: GrampsType) -> Sequence[Sequence[Any]]:
        return obj.get_menu()

    def get_menu_standard_xml(self, obj: GrampsType) -> Sequence[Sequence[Any]]:
        return obj.get_menu_standard_xml()

    @classmethod
    def get_schema(cls) -> dict:
        return GrampsType.get_schema()

    def get_standard_names(self, obj: GrampsType) -> List[str]:
        return obj.get_standard_names()

    def get_standard_xml(self, obj: GrampsType) -> List[str]:
        return obj.get_standard_xml()

    def is_custom(self, obj: GrampsType) -> bool:
        return obj.is_custom()

    def is_default(self, obj: GrampsType) -> bool:
        return obj.is_default()

    def serialize(self, obj: GrampsType) -> Any:
        return obj.serialize()

    def set(self, obj: GrampsType, value: Any) -> None:
        obj.set(value)

    def set_from_xml_str(self, obj: GrampsType, value: str) -> None:
        obj.set_from_xml_str(value)

    def unserialize(self, obj: GrampsType, data: Any) -> None:
        obj.unserialize(data)

    def xml_str(self, obj: GrampsType) -> str:
        return obj.xml_str()

    def value(self, obj: GrampsType) -> int:
        try:
            return obj.value
        except AttributeError:
            return obj.serialize()[self.POS_VALUE]

    def string(self, obj: GrampsType) -> str:
        try:
            return obj.string
        except AttributeError:
            return obj.serialize()[self.POS_STRING]
