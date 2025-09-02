from __future__ import annotations
from typing import Any, List, Tuple, Iterator, Optional, Dict
from gramps.gen.db.base import DbReadBase

class DbReadBaseRepository():

    def close(self, obj) -> None:
        obj.close()

    def db_has_bm_changes(self, obj) -> bool:
        return obj.db_has_bm_changes()

    def find_backlink_handles(self, obj, handle: str, include_classes: Optional[List[str]] = None) -> Iterator[Tuple[str, Optional[str]]]:
        return obj.find_backlink_handles(handle, include_classes)

    def find_initial_person(self, obj) -> Any:
        return obj.find_initial_person()

    def find_next_citation_gramps_id(self, obj) -> str:
        return obj.find_next_citation_gramps_id()

    def find_next_event_gramps_id(self, obj) -> str:
        return obj.find_next_event_gramps_id()

    def find_next_family_gramps_id(self, obj) -> str:
        return obj.find_next_family_gramps_id()

    def find_next_media_gramps_id(self, obj) -> str:
        return obj.find_next_media_gramps_id()

    def find_next_note_gramps_id(self, obj) -> str:
        return obj.find_next_note_gramps_id()

    def find_next_person_gramps_id(self, obj) -> str:
        return obj.find_next_person_gramps_id()

    def find_next_place_gramps_id(self, obj) -> str:
        return obj.find_next_place_gramps_id()

    def find_next_repository_gramps_id(self, obj) -> str:
        return obj.find_next_repository_gramps_id()

    def find_next_source_gramps_id(self, obj) -> str:
        return obj.find_next_source_gramps_id()

    def get_bookmarks(self, obj) -> List[str]:
        return obj.get_bookmarks()

    def get_child_reference_types(self, obj) -> List[Any]:
        return obj.get_child_reference_types()

    def get_citation_bookmarks(self, obj) -> List[str]:
        return obj.get_citation_bookmarks()

    def get_citation_cursor(self, obj) -> Any:
        return obj.get_citation_cursor()

    def get_citation_from_gramps_id(self, obj, val: str) -> Optional[Any]:
        return obj.get_citation_from_gramps_id(val)

    def get_citation_from_handle(self, obj, handle: str) -> Any:
        return obj.get_citation_from_handle(handle)

    def get_citation_handles(self, obj, sort_handles: bool = False, locale: Any = None) -> List[Any]:
        return obj.get_citation_handles(sort_handles, locale)

    def get_dbid(self, obj) -> str:
        return obj.get_dbid()

    def get_dbname(self, obj) -> str:
        return obj.get_dbname()

    def get_default_handle(self, obj) -> Optional[str]:
        return obj.get_default_handle()

    def get_default_person(self, obj) -> Optional[Any]:
        return obj.get_default_person()

    def get_event_attribute_types(self, obj) -> List[Any]:
        return obj.get_event_attribute_types()

    def get_event_bookmarks(self, obj) -> List[str]:
        return obj.get_event_bookmarks()

    def get_event_cursor(self, obj) -> Any:
        return obj.get_event_cursor()

    def get_event_from_gramps_id(self, obj, val: str) -> Optional[Any]:
        return obj.get_event_from_gramps_id(val)

    def get_event_from_handle(self, obj, handle: str) -> Any:
        return obj.get_event_from_handle(handle)

    def get_event_handles(self, obj) -> List[Any]:
        return obj.get_event_handles()

    def get_event_roles(self, obj) -> List[Any]:
        return obj.get_event_roles()

    def get_event_types(self, obj) -> List[Any]:
        return obj.get_event_types()

    def get_family_attribute_types(self, obj) -> List[Any]:
        return obj.get_family_attribute_types()

    def get_family_bookmarks(self, obj) -> List[str]:
        return obj.get_family_bookmarks()

    def get_family_cursor(self, obj) -> Any:
        return obj.get_family_cursor()

    def get_family_event_types(self, obj) -> List[Any]:
        return obj.get_family_event_types()

    def get_family_from_gramps_id(self, obj, val: str) -> Optional[Any]:
        return obj.get_family_from_gramps_id(val)

    def get_family_from_handle(self, obj, handle: str) -> Any:
        return obj.get_family_from_handle(handle)

    def get_family_handles(self, obj, sort_handles: bool = False, locale: Any = None) -> List[Any]:
        return obj.get_family_handles(sort_handles, locale)

    def get_family_relation_types(self, obj) -> List[Any]:
        return obj.get_family_relation_types()

    def get_feature(self, obj, feature: str) -> Any:
        return obj.get_feature(feature)

    def get_media_attribute_types(self, obj) -> List[Any]:
        return obj.get_media_attribute_types()

    def get_media_bookmarks(self, obj) -> List[str]:
        return obj.get_media_bookmarks()

    def get_media_cursor(self, obj) -> Any:
        return obj.get_media_cursor()

    def get_media_from_gramps_id(self, obj, val: str) -> Optional[Any]:
        return obj.get_media_from_gramps_id(val)

    def get_media_from_handle(self, obj, handle: str) -> Any:
        return obj.get_media_from_handle(handle)

    def get_media_handles(self, obj, sort_handles: bool = False, locale: Any = None) -> List[Any]:
        return obj.get_media_handles(sort_handles, locale)

    def get_mediapath(self, obj) -> str:
        return obj.get_mediapath()

    def get_name_group_keys(self, obj) -> List[str]:
        return obj.get_name_group_keys()

    def get_name_group_mapping(self, obj, surname: str) -> Optional[str]:
        return obj.get_name_group_mapping(surname)

    def get_name_types(self, obj) -> List[Any]:
        return obj.get_name_types()

    def get_note_bookmarks(self, obj) -> List[str]:
        return obj.get_note_bookmarks()

    def get_note_cursor(self, obj) -> Any:
        return obj.get_note_cursor()

    def get_note_from_gramps_id(self, obj, val: str) -> Optional[Any]:
        return obj.get_note_from_gramps_id(val)

    def get_note_from_handle(self, obj, handle: str) -> Any:
        return obj.get_note_from_handle(handle)

    def get_note_handles(self, obj) -> List[Any]:
        return obj.get_note_handles()

    def get_note_types(self, obj) -> List[Any]:
        return obj.get_note_types()

    def get_number_of_citations(self, obj) -> int:
        return obj.get_number_of_citations()

    def get_number_of_events(self, obj) -> int:
        return obj.get_number_of_events()

    def get_number_of_families(self, obj) -> int:
        return obj.get_number_of_families()

    def get_number_of_media(self, obj) -> int:
        return obj.get_number_of_media()

    def get_number_of_notes(self, obj) -> int:
        return obj.get_number_of_notes()

    def get_number_of_people(self, obj) -> int:
        return obj.get_number_of_people()

    def get_number_of_places(self, obj) -> int:
        return obj.get_number_of_places()

    def get_number_of_repositories(self, obj) -> int:
        return obj.get_number_of_repositories()

    def get_number_of_sources(self, obj) -> int:
        return obj.get_number_of_sources()

    def get_number_of_tags(self, obj) -> int:
        return obj.get_number_of_tags()

    def get_origin_types(self, obj) -> List[Any]:
        return obj.get_origin_types()

    def get_person_attribute_types(self, obj) -> List[Any]:
        return obj.get_person_attribute_types()

    def get_person_cursor(self, obj) -> Any:
        return obj.get_person_cursor()

    def get_person_event_types(self, obj) -> List[Any]:
        return obj.get_person_event_types()

    def get_person_from_gramps_id(self, obj, val: str) -> Optional[Any]:
        return obj.get_person_from_gramps_id(val)

    def get_person_from_handle(self, obj, handle: str) -> Any:
        return obj.get_person_from_handle(handle)

    def get_person_handles(self, obj, sort_handles: bool = False, locale: Any = None) -> List[Any]:
        return obj.get_person_handles(sort_handles, locale)

    def get_place_bookmarks(self, obj) -> List[str]:
        return obj.get_place_bookmarks()

    def get_place_cursor(self, obj) -> Any:
        return obj.get_place_cursor()

    def get_place_from_gramps_id(self, obj, val: str) -> Optional[Any]:
        return obj.get_place_from_gramps_id(val)

    def get_place_from_handle(self, obj, handle: str) -> Any:
        return obj.get_place_from_handle(handle)

    def get_place_handles(self, obj, sort_handles: bool = False, locale: Any = None) -> List[Any]:
        return obj.get_place_handles(sort_handles, locale)

    def get_place_tree_cursor(self, obj) -> Any:
        return obj.get_place_tree_cursor()

    def get_place_types(self, obj) -> List[Any]:
        return obj.get_place_types()

    def get_raw_citation_data(self, obj, handle: str) -> Any:
        return obj.get_raw_citation_data(handle)

    def get_raw_event_data(self, obj, handle: str) -> Any:
        return obj.get_raw_event_data(handle)

    def get_raw_family_data(self, obj, handle: str) -> Any:
        return obj.get_raw_family_data(handle)

    def get_raw_media_data(self, obj, handle: str) -> Any:
        return obj.get_raw_media_data(handle)

    def get_raw_note_data(self, obj, handle: str) -> Any:
        return obj.get_raw_note_data(handle)

    def get_raw_person_data(self, obj, handle: str) -> Any:
        return obj.get_raw_person_data(handle)

    def get_raw_place_data(self, obj, handle: str) -> Any:
        return obj.get_raw_place_data(handle)

    def get_raw_repository_data(self, obj, handle: str) -> Any:
        return obj.get_raw_repository_data(handle)

    def get_raw_source_data(self, obj, handle: str) -> Any:
        return obj.get_raw_source_data(handle)

    def get_raw_tag_data(self, obj, handle: str) -> Any:
        return obj.get_raw_tag_data(handle)

    def get_repo_bookmarks(self, obj) -> List[str]:
        return obj.get_repo_bookmarks()

    def get_repository_cursor(self, obj) -> Any:
        return obj.get_repository_cursor()

    def get_repository_from_gramps_id(self, obj, val: str) -> Optional[Any]:
        return obj.get_repository_from_gramps_id(val)

    def get_repository_from_handle(self, obj, handle: str) -> Any:
        return obj.get_repository_from_handle(handle)

    def get_repository_handles(self, obj) -> List[Any]:
        return obj.get_repository_handles()

    def get_repository_types(self, obj) -> List[Any]:
        return obj.get_repository_types()

    def get_researcher(self, obj) -> Any:
        return obj.get_researcher()

    def get_save_path(self, obj) -> str:
        return obj.get_save_path()

    def get_source_attribute_types(self, obj) -> List[Any]:
        return obj.get_source_attribute_types()

    def get_source_bookmarks(self, obj) -> List[str]:
        return obj.get_source_bookmarks()

    def get_source_cursor(self, obj) -> Any:
        return obj.get_source_cursor()

    def get_source_from_gramps_id(self, obj, val: str) -> Optional[Any]:
        return obj.get_source_from_gramps_id(val)

    def get_source_from_handle(self, obj, handle: str) -> Any:
        return obj.get_source_from_handle(handle)

    def get_source_handles(self, obj, sort_handles: bool = False, locale: Any = None) -> List[Any]:
        return obj.get_source_handles(sort_handles, locale)

    def get_source_media_types(self, obj) -> List[Any]:
        return obj.get_source_media_types()

    def get_summary(self, obj) -> Dict[str, Any]:
        return obj.get_summary()

    def get_surname_list(self, obj) -> List[str]:
        return obj.get_surname_list()

    def get_tag_cursor(self, obj) -> Any:
        return obj.get_tag_cursor()

    def get_tag_from_handle(self, obj, handle: str) -> Any:
        return obj.get_tag_from_handle(handle)

    def get_tag_from_name(self, obj, val: str) -> Optional[Any]:
        return obj.get_tag_from_name(val)

    def get_tag_handles(self, obj, sort_handles: bool = False, locale: Any = None) -> List[Any]:
        return obj.get_tag_handles(sort_handles, locale)

    def get_url_types(self, obj) -> List[Any]:
        return obj.get_url_types()

    def has_citation_gramps_id(self, obj, gramps_id: str) -> bool:
        return obj.has_citation_gramps_id(gramps_id)

    def has_citation_handle(self, obj, handle: str) -> bool:
        return obj.has_citation_handle(handle)

    def has_event_gramps_id(self, obj, gramps_id: str) -> bool:
        return obj.has_event_gramps_id(gramps_id)

    def has_event_handle(self, obj, handle: str) -> bool:
        return obj.has_event_handle(handle)

    def has_family_gramps_id(self, obj, gramps_id: str) -> bool:
        return obj.has_family_gramps_id(gramps_id)

    def has_family_handle(self, obj, handle: str) -> bool:
        return obj.has_family_handle(handle)

    def has_media_gramps_id(self, obj, gramps_id: str) -> bool:
        return obj.has_media_gramps_id(gramps_id)

    def has_media_handle(self, obj, handle: str) -> bool:
        return obj.has_media_handle(handle)

    def has_name_group_key(self, obj, name: str) -> bool:
        return obj.has_name_group_key(name)

    def has_note_gramps_id(self, obj, gramps_id: str) -> bool:
        return obj.has_note_gramps_id(gramps_id)

    def has_note_handle(self, obj, handle: str) -> bool:
        return obj.has_note_handle(handle)

    def has_person_gramps_id(self, obj, gramps_id: str) -> bool:
        return obj.has_person_gramps_id(gramps_id)

    def has_person_handle(self, obj, handle: str) -> bool:
        return obj.has_person_handle(handle)

    def has_place_gramps_id(self, obj, gramps_id: str) -> bool:
        return obj.has_place_gramps_id(gramps_id)

    def has_place_handle(self, obj, handle: str) -> bool:
        return obj.has_place_handle(handle)

    def has_repository_gramps_id(self, obj, gramps_id: str) -> bool:
        return obj.has_repository_gramps_id(gramps_id)

    def has_repository_handle(self, obj, handle: str) -> bool:
        return obj.has_repository_handle(handle)

    def has_source_gramps_id(self, obj, gramps_id: str) -> bool:
        return obj.has_source_gramps_id(gramps_id)

    def has_source_handle(self, obj, handle: str) -> bool:
        return obj.has_source_handle(handle)

    def has_tag_handle(self, obj, handle: str) -> bool:
        return obj.has_tag_handle(handle)

    def is_open(self, obj) -> bool:
        return obj.is_open()

    def iter_citation_handles(self, obj) -> Iterator[str]:
        return obj.iter_citation_handles()

    def iter_citations(self, obj) -> Iterator[Any]:
        return obj.iter_citations()

    def iter_event_handles(self, obj) -> Iterator[str]:
        return obj.iter_event_handles()

    def iter_events(self, obj) -> Iterator[Any]:
        return obj.iter_events()

    def iter_families(self, obj) -> Iterator[Any]:
        return obj.iter_families()

    def iter_family_handles(self, obj) -> Iterator[str]:
        return obj.iter_family_handles()

    def iter_media(self, obj) -> Iterator[Any]:
        return obj.iter_media()

    def iter_media_handles(self, obj) -> Iterator[str]:
        return obj.iter_media_handles()

    def iter_note_handles(self, obj) -> Iterator[str]:
        return obj.iter_note_handles()

    def iter_notes(self, obj) -> Iterator[Any]:
        return obj.iter_notes()

    def iter_people(self, obj) -> Iterator[Any]:
        return obj.iter_people()

    def iter_person_handles(self, obj) -> Iterator[str]:
        return obj.iter_person_handles()

    def iter_place_handles(self, obj) -> Iterator[str]:
        return obj.iter_place_handles()

    def iter_places(self, obj) -> Iterator[Any]:
        return obj.iter_places()

    def iter_repositories(self, obj) -> Iterator[Any]:
        return obj.iter_repositories()

    def iter_repository_handles(self, obj) -> Iterator[str]:
        return obj.iter_repository_handles()

    def iter_source_handles(self, obj) -> Iterator[str]:
        return obj.iter_source_handles()

    def iter_sources(self, obj) -> Iterator[Any]:
        return obj.iter_sources()

    def iter_tag_handles(self, obj) -> Iterator[str]:
        return obj.iter_tag_handles()

    def iter_tags(self, obj) -> Iterator[Any]:
        return obj.iter_tags()

    def load(self, obj, name: str, callback: Any, mode: Optional[str] = None, force_schema_upgrade: bool = False, force_bsddb_upgrade: bool = False) -> None:
        obj.load(name, callback, mode=mode, force_schema_upgrade=force_schema_upgrade, force_bsddb_upgrade=force_bsddb_upgrade)

    def method(self, obj, fmt: str, *args: str) -> Optional[Any]:
        return obj.method(fmt, *args)

    def report_bm_change(self, obj) -> None:
        obj.report_bm_change()

    def request_rebuild(self, obj) -> None:
        obj.request_rebuild()

    def requires_login(self, obj) -> bool:
        return obj.requires_login()

    def set_citation_id_prefix(self, obj, val: str) -> None:
        obj.set_citation_id_prefix(val)

    def set_event_id_prefix(self, obj, val: str) -> None:
        obj.set_event_id_prefix(val)

    def set_family_id_prefix(self, obj, val: str) -> None:
        obj.set_family_id_prefix(val)

    def set_feature(self, obj, feature: str, value: Any) -> None:
        obj.set_feature(feature, value)

    def set_media_id_prefix(self, obj, val: str) -> None:
        obj.set_media_id_prefix(val)

    def set_mediapath(self, obj, path: str) -> None:
        obj.set_mediapath(path)

    def set_note_id_prefix(self, obj, val: str) -> None:
        obj.set_note_id_prefix(val)

    def set_person_id_prefix(self, obj, val: str) -> None:
        obj.set_person_id_prefix(val)

    def set_place_id_prefix(self, obj, val: str) -> None:
        obj.set_place_id_prefix(val)

    def set_prefixes(self, obj, person: str, media: str, family: str, source: str, citation: str, place: str, event: str, repository: str, note: str) -> None:
        obj.set_prefixes(person, media, family, source, citation, place, event, repository, note)

    def set_repository_id_prefix(self, obj, val: str) -> None:
        obj.set_repository_id_prefix(val)

    def set_researcher(self, obj, owner: Any) -> None:
        obj.set_researcher(owner)

    def set_source_id_prefix(self, obj, val: str) -> None:
        obj.set_source_id_prefix(val)

    def version_supported(self, obj) -> bool:
        return obj.version_supported()