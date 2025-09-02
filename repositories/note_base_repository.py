from __future__ import annotations

from typing import Any, List, Tuple

from repositories.repository_core import RepositoryCore


class NoteBaseRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def add_note(self, obj, handle: str) -> bool:
        return obj.add_note(handle)

    def get_note_child_list(self, obj) -> List[Any]:
        return obj.get_note_child_list()

    def get_note_list(self, obj) -> List[str]:
        return obj.get_note_list()

    def get_referenced_note_handles(self, obj) -> List[Tuple[str, str]]:
        return obj.get_referenced_note_handles()

    def has_note_reference(self, obj, note_handle: str) -> bool:
        return obj.has_note_reference(note_handle)

    def remove_note(self, obj, handle: str) -> None:
        obj.remove_note(handle)

    def replace_note_references(self, obj, old_handle: str, new_handle: str) -> None:
        obj.replace_note_references(old_handle, new_handle)

    def serialize(self, obj) -> Any:
        return obj.serialize()

    def set_note_list(self, obj, note_list: List[str]) -> None:
        obj.set_note_list(note_list)

    def unserialize(self, obj, data: Any) -> None:
        obj.unserialize(data)

    def note_list(self, obj) -> List[str]:
        try:
            return obj.note_list
        except AttributeError:
            return obj.get_note_list()
