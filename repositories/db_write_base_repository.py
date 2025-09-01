from __future__ import annotations
from typing import Any, Optional, Sequence
from gramps.gen.db.base import DbWriteBase
from repositories.db_read_base_repository import DbReadBaseRepository

class DbWriteBaseRepository(DbReadBaseRepository):

    def add_child_to_family(self, obj: DbWriteBase, family: Any, child: Any, mrel: Any, frel: Any, trans: Any = None) -> None:
        obj.add_child_to_family(family, child, mrel, frel, trans)

    def add_citation(self, obj: DbWriteBase, event: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_citation(event, transaction, set_gid=set_gid)

    def add_event(self, obj: DbWriteBase, event: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_event(event, transaction, set_gid=set_gid)

    def add_family(self, obj: DbWriteBase, family: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_family(family, transaction, set_gid=set_gid)

    def add_media(self, obj: DbWriteBase, obj_media: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_media(obj_media, transaction, set_gid=set_gid)

    def add_note(self, obj: DbWriteBase, note: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_note(note, transaction, set_gid=set_gid)

    def add_person(self, obj: DbWriteBase, person: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_person(person, transaction, set_gid=set_gid)

    def add_place(self, obj: DbWriteBase, place: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_place(place, transaction, set_gid=set_gid)

    def add_repository(self, obj: DbWriteBase, repo: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_repository(repo, transaction, set_gid=set_gid)

    def add_source(self, obj: DbWriteBase, source: Any, transaction: Any, set_gid: bool = True) -> None:
        obj.add_source(source, transaction, set_gid=set_gid)

    def add_tag(self, obj: DbWriteBase, tag: Any, transaction: Any) -> None:
        obj.add_tag(tag, transaction)

    def add_to_surname_list(self, obj: DbWriteBase, person: Any, batch_transaction: Any, name: str) -> None:
        obj.add_to_surname_list(person, batch_transaction, name)

    def commit_citation(self, obj: DbWriteBase, event: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_citation(event, transaction, change_time=change_time)

    def commit_event(self, obj: DbWriteBase, event: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_event(event, transaction, change_time=change_time)

    def commit_family(self, obj: DbWriteBase, family: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_family(family, transaction, change_time=change_time)

    def commit_media(self, obj: DbWriteBase, obj_media: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_media(obj_media, transaction, change_time=change_time)

    def commit_note(self, obj: DbWriteBase, note: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_note(note, transaction, change_time=change_time)

    def commit_person(self, obj: DbWriteBase, person: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_person(person, transaction, change_time=change_time)

    def commit_place(self, obj: DbWriteBase, place: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_place(place, transaction, change_time=change_time)

    def commit_repository(self, obj: DbWriteBase, repository: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_repository(repository, transaction, change_time=change_time)

    def commit_source(self, obj: DbWriteBase, source: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_source(source, transaction, change_time=change_time)

    def commit_tag(self, obj: DbWriteBase, tag: Any, transaction: Any, change_time: Any = None) -> None:
        obj.commit_tag(tag, transaction, change_time=change_time)

    def delete_person_from_database(self, obj: DbWriteBase, person: Any, trans: Any) -> None:
        obj.delete_person_from_database(person, trans)

    def get_total(self, obj: DbWriteBase) -> int:
        return obj.get_total()

    def get_undodb(self, obj: DbWriteBase) -> Any:
        return obj.get_undodb()

    def marriage_from_eventref_list(self, obj: DbWriteBase, eventref_list: Sequence[Any]) -> Optional[Any]:
        return obj.marriage_from_eventref_list(eventref_list)

    def rebuild_secondary(self, obj: DbWriteBase, callback: Any) -> None:
        obj.rebuild_secondary(callback)

    def redo(self, obj: DbWriteBase, update_history: bool = True) -> None:
        obj.redo(update_history=update_history)

    def reindex_reference_map(self, obj: DbWriteBase, callback: Any) -> None:
        obj.reindex_reference_map(callback)

    def remove_child_from_family(self, obj: DbWriteBase, person_handle: str, family_handle: str, trans: Any = None) -> None:
        obj.remove_child_from_family(person_handle, family_handle, trans)

    def remove_citation(self, obj: DbWriteBase, handle: str, transaction: Any) -> None:
        obj.remove_citation(handle, transaction)

    def remove_event(self, obj: DbWriteBase, handle: str, transaction: Any) -> None:
        obj.remove_event(handle, transaction)

    def remove_family(self, obj: DbWriteBase, handle: str, transaction: Any) -> None:
        obj.remove_family(handle, transaction)

    def remove_family_relationships(self, obj: DbWriteBase, family_handle: str, trans: Any = None) -> None:
        obj.remove_family_relationships(family_handle, trans)

    def remove_from_surname_list(self, obj: DbWriteBase, person: Any) -> None:
        obj.remove_from_surname_list(person)

    def remove_media(self, obj: DbWriteBase, handle: str, transaction: Any) -> None:
        obj.remove_media(handle, transaction)

    def remove_note(self, obj: DbWriteBase, handle: str, transaction: Any) -> None:
        obj.remove_note(handle, transaction)

    def remove_parent_from_family(self, obj: DbWriteBase, person_handle: str, family_handle: str, trans: Any = None) -> None:
        obj.remove_parent_from_family(person_handle, family_handle, trans)

    def remove_person(self, obj: DbWriteBase, handle: str, transaction: Any) -> None:
        obj.remove_person(handle, transaction)

    def remove_place(self, obj: DbWriteBase, handle: str, transaction: Any) -> None:
        obj.remove_place(handle, transaction)

    def remove_repository(self, obj: DbWriteBase, handle: str, transaction: Any) -> None:
        obj.remove_repository(handle, transaction)

    def remove_source(self, obj: DbWriteBase, handle: str, transaction: Any) -> None:
        obj.remove_source(handle, transaction)

    def remove_tag(self, obj: DbWriteBase, handle: str, transaction: Any) -> None:
        obj.remove_tag(handle, transaction)

    def set_birth_death_index(self, obj: DbWriteBase, person: Any) -> None:
        obj.set_birth_death_index(person)

    def set_default_person_handle(self, obj: DbWriteBase, handle: str) -> None:
        obj.set_default_person_handle(handle)

    def set_name_group_mapping(self, obj: DbWriteBase, name: str, group: str) -> None:
        obj.set_name_group_mapping(name, group)

    def transaction_abort(self, obj: DbWriteBase, transaction: Any) -> None:
        obj.transaction_abort(transaction)

    def transaction_begin(self, obj: DbWriteBase, transaction: Any) -> Any:
        return obj.transaction_begin(transaction)

    def transaction_commit(self, obj: DbWriteBase, transaction: Any) -> None:
        obj.transaction_commit(transaction)

    def undo(self, obj: DbWriteBase, update_history: bool = True) -> None:
        obj.undo(update_history=update_history)