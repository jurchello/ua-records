from __future__ import annotations
from typing import Any, List, Tuple
from gramps.gen.lib.name import Name
from repositories.secondary_object_repository import SecondaryObjectRepository
from repositories.privacy_base_repository import PrivacyBaseRepository
from repositories.surname_base_repository import SurnameBaseRepository
from repositories.citation_base_repository import CitationBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.date_base_repository import DateBaseRepository

class NameRepository(
    SecondaryObjectRepository,
    PrivacyBaseRepository,
    SurnameBaseRepository,
    CitationBaseRepository,
    NoteBaseRepository,
    DateBaseRepository,
):
    DEF = 0
    FN = 4
    FNLN = 2
    LNFN = 1
    LNFNP = 5
    NAMEFORMATS = (0, 1, 2, 4, 5)
    PTFN = 3

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_call_name(self, obj) -> str:
        return obj.get_call_name()

    def get_display_as(self, obj) -> int:
        return obj.get_display_as()

    def get_family_nick_name(self, obj) -> str:
        return obj.get_family_nick_name()

    def get_first_name(self, obj) -> str:
        return obj.get_first_name()

    def get_gedcom_name(self, obj) -> str:
        return obj.get_gedcom_name()

    def get_gedcom_parts(self, obj) -> dict:
        return obj.get_gedcom_parts()

    def get_group_as(self, obj) -> str:
        return obj.get_group_as()

    def get_group_name(self, obj) -> str:
        return obj.get_group_name()

    def get_handle_referents(self, obj) -> List[Any]:
        return obj.get_handle_referents()

    def get_name(self, obj) -> str:
        return obj.get_name()

    def get_nick_name(self, obj) -> str:
        return obj.get_nick_name()

    def get_note_child_list(self, obj) -> List[Any]:
        return obj.get_note_child_list()

    def get_referenced_handles(self, obj) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    def get_regular_name(self, obj) -> str:
        return obj.get_regular_name()

    @classmethod
    def get_schema(cls) -> dict:
        return Name.get_schema()

    def get_sort_as(self, obj) -> int:
        return obj.get_sort_as()

    def get_suffix(self, obj) -> str:
        return obj.get_suffix()

    def get_text_data_child_list(self, obj) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj) -> List[Any]:
        return obj.get_text_data_list()

    def get_title(self, obj) -> str:
        return obj.get_title()

    def get_type(self, obj) -> Any:
        return obj.get_type()

    def get_upper_name(self, obj) -> str:
        return obj.get_upper_name()

    def is_empty(self, obj) -> bool:
        return obj.is_empty()

    def is_equivalent(self, obj, other) -> int:
        return obj.is_equivalent(other)

    def merge(self, obj, acquisition) -> None:
        obj.merge(acquisition)

    def serialize(self, obj) -> Any:
        return obj.serialize()

    def set_call_name(self, obj, val: str) -> None:
        obj.set_call_name(val)

    def set_display_as(self, obj, value: int) -> None:
        obj.set_display_as(value)

    def set_family_nick_name(self, obj, val: str) -> None:
        obj.set_family_nick_name(val)

    def set_first_name(self, obj, name: str) -> None:
        obj.set_first_name(name)

    def set_group_as(self, obj, name: str) -> None:
        obj.set_group_as(name)

    def set_nick_name(self, obj, val: str) -> None:
        obj.set_nick_name(val)

    def set_sort_as(self, obj, value: int) -> None:
        obj.set_sort_as(value)

    def set_suffix(self, obj, name: str) -> None:
        obj.set_suffix(name)

    def set_title(self, obj, title: str) -> None:
        obj.set_title(title)

    def set_type(self, obj, the_type: Any) -> None:
        obj.set_type(the_type)

    def unserialize(self, obj, data: Any) -> None:
        obj.unserialize(data)