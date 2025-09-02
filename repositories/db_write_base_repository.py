from __future__ import annotations
from typing import Any, Optional, Sequence
from gramps.gen.db.base import DbWriteBase
from repositories.db_read_base_repository import DbReadBaseRepository

class DbWriteBaseRepository(DbReadBaseRepository):

    def add_child_to_family(self, obj, family: Any, child: Any, mrel: Any, frel: Any, trans: Any = None) -> None:
        obj.add_child_to_family(family, child, mrel, frel, trans)

    def add_citation(self, obj, event: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_citation(event, transaction, set_gid=set_gid)

    def add_event(self, obj, event: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_event(event, transaction, set_gid=set_gid)

    def add_family(self, obj, family: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_family(family, transaction, set_gid=set_gid)

    def add_media(self, obj, obj_media: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_media(obj_media, transaction, set_gid=set_gid)

    def add_note(self, obj, note: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_note(note, transaction, set_gid=set_gid)

    def add_person(self, obj, person: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_person(person, transaction, set_gid=set_gid)

    def add_place(self, obj, place: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_place(place, transaction, set_gid=set_gid)

    def add_repository(self, obj, repo: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_repository(repo, transaction, set_gid=set_gid)

    def add_source(self, obj, source: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_source(source, transaction, set_gid=set_gid)

    def add_tag(self, obj, tag: Any, transaction: Any) -> None:
        obj.add_tag(tag, transaction)

    def add_to_surname_list(self, obj, person: Any, batch_transaction: Any, name: str) -> None:
        obj.add_to_surname_list(person, batch_transaction, name)

    def commit_citation(self, obj, event: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_citation(event, transaction, change_time=change_time)

    def commit_event(self, obj, event: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_event(event, transaction, change_time=change_time)

    def commit_family(self, obj, family: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_family(family, transaction, change_time=change_time)

    def commit_media(self, obj, obj_media: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_media(obj_media, transaction, change_time=change_time)

    def commit_note(self, obj, note: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_note(note, transaction, change_time=change_time)

    def commit_person(self, obj, person: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_person(person, transaction, change_time=change_time)

    def commit_place(self, obj, place: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_place(place, transaction, change_time=change_time)

    def commit_repository(self, obj, repository: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_repository(repository, transaction, change_time=change_time)

    def commit_source(self, obj, source: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_source(source, transaction, change_time=change_time)

    def commit_tag(self, obj, tag: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_tag(tag, transaction, change_time=change_time)

    def delete_person_from_database(self, obj, person: Any, trans: Any) -> None:
        obj.delete_person_from_database(person, trans)

    def get_total(self, obj) -> int:
        return obj.get_total()

    def get_undodb(self, obj) -> Any:
        return obj.get_undodb()

    def marriage_from_eventref_list(self, obj, eventref_list: Sequence[Any]) -> Optional[Any]:
        return obj.marriage_from_eventref_list(eventref_list)

    def rebuild_secondary(self, obj, callback: Any) -> None:
        obj.rebuild_secondary(callback)

    def redo(self, obj, update_history: bool = True) -> None:
        obj.redo(update_history=update_history)

    def reindex_reference_map(self, obj, callback: Any) -> None:
        obj.reindex_reference_map(callback)

    def remove_child_from_family(self, obj, person_handle: str, family_handle: str, trans: Any = None) -> None:
        obj.remove_child_from_family(person_handle, family_handle, trans)

    def remove_citation(self, obj, handle: str, transaction: Any) -> None:
        obj.remove_citation(handle, transaction)

    def remove_event(self, obj, handle: str, transaction: Any) -> None:
        obj.remove_event(handle, transaction)

    def remove_family(self, obj, handle: str, transaction: Any) -> None:
        obj.remove_family(handle, transaction)

    def remove_family_relationships(self, obj, family_handle: str, trans: Any = None) -> None:
        obj.remove_family_relationships(family_handle, trans)

    def remove_from_surname_list(self, obj, person: Any) -> None:
        obj.remove_from_surname_list(person)

    def remove_media(self, obj, handle: str, transaction: Any) -> None:
        obj.remove_media(handle, transaction)

    def remove_note(self, obj, handle: str, transaction: Any) -> None:
        obj.remove_note(handle, transaction)

    def remove_parent_from_family(self, obj, person_handle: str, family_handle: str, trans: Any = None) -> None:
        obj.remove_parent_from_family(person_handle, family_handle, trans)

    def remove_person(self, obj, handle: str, transaction: Any) -> None:
        obj.remove_person(handle, transaction)

    def remove_place(self, obj, handle: str, transaction: Any) -> None:
        obj.remove_place(handle, transaction)

    def remove_repository(self, obj, handle: str, transaction: Any) -> None:
        obj.remove_repository(handle, transaction)

    def remove_source(self, obj, handle: str, transaction: Any) -> None:
        obj.remove_source(handle, transaction)

    def remove_tag(self, obj, handle: str, transaction: Any) -> None:
        obj.remove_tag(handle, transaction)

    def set_birth_death_index(self, obj, person: Any) -> None:
        obj.set_birth_death_index(person)

    def set_default_person_handle(self, obj, handle: str) -> None:
        obj.set_default_person_handle(handle)

    def set_name_group_mapping(self, obj, name: str, group: str) -> None:
        obj.set_name_group_mapping(name, group)

    def transaction_abort(self, obj, transaction: Any) -> None:
        obj.transaction_abort(transaction)

    def transaction_begin(self, obj, transaction: Any) -> Any:
        return obj.transaction_begin(transaction)

    def transaction_commit(self, obj, transaction: Any) -> None:
        obj.transaction_commit(transaction)

    def undo(self, obj, update_history: bool = True) -> None:
        obj.undo(update_history=update_history)