from __future__ import annotations
from typing import Any, List, Dict, Tuple, Optional, Iterable
from gramps.gen.lib import Person
from repositories.citation_base_repository import CitationBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.attribute_base_repository import AttributeBaseRepository
from repositories.media_base_repository import MediaBaseRepository
from repositories.address_base_repository import AddressBaseRepository
from repositories.url_base_repository import UrlBaseRepository
from repositories.lds_ord_base_repository import LdsOrdBaseRepository
from repositories.primary_object_repository import PrimaryObjectRepository

class PersonRepository(
    CitationBaseRepository, 
    NoteBaseRepository, 
    AttributeBaseRepository, 
    MediaBaseRepository, 
    AddressBaseRepository, 
    UrlBaseRepository, 
    LdsOrdBaseRepository, 
    PrimaryObjectRepository
):
    FEMALE = 0
    MALE = 1
    UNKNOWN = 2

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def add_alternate_name(self, obj: Person, name: Any) -> None:
        obj.add_alternate_name(name)

    def add_event_ref(self, obj: Person, event_ref: Any) -> None:
        obj.add_event_ref(event_ref)

    def add_family_handle(self, obj: Person, family_handle: str) -> None:
        obj.add_family_handle(family_handle)

    def add_parent_family_handle(self, obj: Person, family_handle: str) -> None:
        obj.add_parent_family_handle(family_handle)

    def add_person_ref(self, obj: Person, person_ref: Any) -> None:
        obj.add_person_ref(person_ref)

    def clear_family_handle_list(self, obj: Person) -> None:
        obj.clear_family_handle_list()

    def clear_parent_family_handle_list(self, obj: Person) -> None:
        obj.clear_parent_family_handle_list()

    def get_alternate_names(self, obj: Person) -> List[Any]:
        return obj.get_alternate_names()

    def get_birth_ref(self, obj: Person) -> Optional[Any]:
        return obj.get_birth_ref()

    def get_citation_child_list(self, obj: Person) -> List[Any]:
        return obj.get_citation_child_list()

    def get_death_ref(self, obj: Person) -> Optional[Any]:
        return obj.get_death_ref()

    def get_event_ref_list(self, obj: Person) -> List[Any]:
        return obj.get_event_ref_list()

    def get_family_handle_list(self, obj: Person) -> List[str]:
        return obj.get_family_handle_list()

    def get_gender(self, obj: Person) -> int:
        return obj.get_gender()

    def get_handle_referents(self, obj: Person) -> List[Any]:
        return obj.get_handle_referents()

    def get_main_parents_family_handle(self, obj: Person) -> Optional[str]:
        return obj.get_main_parents_family_handle()

    def get_nick_name(self, obj: Person) -> Optional[str]:
        return obj.get_nick_name()

    def get_note_child_list(self, obj: Person) -> List[Any]:
        return obj.get_note_child_list()

    def get_parent_family_handle_list(self, obj: Person) -> List[str]:
        return obj.get_parent_family_handle_list()

    def get_person_ref_list(self, obj: Person) -> List[Any]:
        return obj.get_person_ref_list()

    def get_primary_event_ref_list(self, obj: Person) -> Iterable[Any]:
        return obj.get_primary_event_ref_list()

    def get_primary_name(self, obj: Person) -> Any:
        return obj.get_primary_name()

    def get_referenced_handles(self, obj: Person) -> List[Tuple[str, Optional[str]]]:
        return obj.get_referenced_handles()

    def get_schema(self) -> Dict[str, Any]:
        return Person.get_schema()

    def get_text_data_child_list(self, obj: Person) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj: Person) -> List[str]:
        return obj.get_text_data_list()

    def merge(self, obj: Person, acquisition: Person) -> None:
        obj.merge(acquisition)

    def remove_family_handle(self, obj: Person, family_handle: str) -> bool:
        return obj.remove_family_handle(family_handle)

    def remove_parent_family_handle(self, obj: Person, family_handle: str) -> Optional[Tuple[str, str, str]]:
        res: Any = obj.remove_parent_family_handle(family_handle)
        if isinstance(res, tuple):
            return res
        return None

    def serialize(self, obj: Person) -> Tuple[Any, ...]:
        return obj.serialize()

    def set_alternate_names(self, obj: Person, alt_name_list: List[Any]) -> None:
        obj.set_alternate_names(alt_name_list)

    def set_birth_ref(self, obj: Person, event_ref: Any) -> None:
        obj.set_birth_ref(event_ref)

    def set_death_ref(self, obj: Person, event_ref: Any) -> None:
        obj.set_death_ref(event_ref)

    def set_event_ref_list(self, obj: Person, event_ref_list: List[Any]) -> None:
        obj.set_event_ref_list(event_ref_list)

    def set_family_handle_list(self, obj: Person, family_list: List[str]) -> None:
        obj.set_family_handle_list(family_list)

    def set_gender(self, obj: Person, gender: int) -> None:
        obj.set_gender(gender)

    def set_main_parent_family_handle(self, obj: Person, family_handle: str) -> bool:
        return obj.set_main_parent_family_handle(family_handle)

    def set_parent_family_handle_list(self, obj: Person, family_list: List[str]) -> None:
        obj.set_parent_family_handle_list(family_list)

    def set_person_ref_list(self, obj: Person, person_ref_list: List[Any]) -> None:
        obj.set_person_ref_list(person_ref_list)

    def set_preferred_family_handle(self, obj: Person, family_handle: str) -> bool:
        return obj.set_preferred_family_handle(family_handle)

    def set_primary_name(self, obj: Person, name: Any) -> None:
        obj.set_primary_name(name)

    def unserialize(self, obj: Person, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)