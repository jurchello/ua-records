from __future__ import annotations
from typing import Any, List, Dict, Tuple
from gramps.gen.lib import Place
from repositories.citation_base_repository import CitationBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.media_base_repository import MediaBaseRepository
from repositories.primary_object_repository import PrimaryObjectRepository

class PlaceRepository(
    CitationBaseRepository, 
    NoteBaseRepository, 
    MediaBaseRepository, 
    PrimaryObjectRepository
):
    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def add_alternate_locations(self, obj, location: Any) -> None:
        obj.add_alternate_locations(location)

    def add_alternative_name(self, obj, name: str) -> None:
        obj.add_alternative_name(name)

    def add_placeref(self, obj, placeref: Any) -> None:
        obj.add_placeref(placeref)

    def get_all_names(self, obj) -> List[Any]:
        return obj.get_all_names()

    def get_alternate_locations(self, obj) -> List[Any]:
        return obj.get_alternate_locations()

    def get_alternative_names(self, obj) -> List[Any]:
        return obj.get_alternative_names()

    def get_citation_child_list(self, obj) -> List[Any]:
        return obj.get_citation_child_list()

    def get_code(self, obj) -> str:
        return obj.get_code()

    def get_handle_referents(self, obj) -> List[Any]:
        return obj.get_handle_referents()

    def get_latitude(self, obj) -> str:
        return obj.get_latitude()

    def get_longitude(self, obj) -> str:
        return obj.get_longitude()

    def get_name(self, obj) -> Any:
        return obj.get_name()

    def get_note_child_list(self, obj) -> List[Any]:
        return obj.get_note_child_list()

    def get_placeref_list(self, obj) -> List[Any]:
        return obj.get_placeref_list()

    def get_referenced_handles(self, obj) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    def get_schema(self) -> Dict[str, Any]:
        return Place.get_schema()

    def get_text_data_child_list(self, obj) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj) -> List[str]:
        return obj.get_text_data_list()

    def get_title(self, obj) -> str:
        return obj.get_title()

    def get_type(self, obj) -> Any:
        return obj.get_type()

    def merge(self, obj, acquisition) -> None:
        obj.merge(acquisition)

    def serialize(self, obj) -> Tuple[Any, ...]:
        return obj.serialize()

    def set_alternate_locations(self, obj, location_list: List[Any]) -> None:
        obj.set_alternate_locations(location_list)

    def set_alternative_names(self, obj, name_list: List[Any]) -> None:
        obj.set_alternative_names(name_list)

    def set_code(self, obj, code: str) -> None:
        obj.set_code(code)

    def set_latitude(self, obj, latitude: str) -> None:
        obj.set_latitude(latitude)

    def set_longitude(self, obj, longitude: str) -> None:
        obj.set_longitude(longitude)

    def set_name(self, obj, name: Any) -> None:
        obj.set_name(name)

    def set_placeref_list(self, obj, placeref_list: List[Any]) -> None:
        obj.set_placeref_list(placeref_list)

    def set_title(self, obj, title: str) -> None:
        obj.set_title(title)

    def set_type(self, obj, place_type: Any) -> None:
        obj.set_type(place_type)

    def unserialize(self, obj, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)