from __future__ import annotations

from typing import Any, List, Tuple

from gramps.gen.lib import TagBase

from repositories.repository_core import RepositoryCore


class TagBaseRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def add_tag(self, obj: TagBase, tag: str) -> None:
        obj.add_tag(tag)

    def get_referenced_tag_handles(self, obj: TagBase) -> List[Tuple[str, str]]:
        return obj.get_referenced_tag_handles()

    def get_tag_list(self, obj: TagBase) -> List[str]:
        return obj.get_tag_list()

    def remove_tag(self, obj: TagBase, tag: str) -> bool:
        return obj.remove_tag(tag)

    def replace_tag_references(self, obj: TagBase, old_handle: str, new_handle: str) -> None:
        obj.replace_tag_references(old_handle, new_handle)

    def set_tag_list(self, obj: TagBase, tag_list: List[str]) -> None:
        obj.set_tag_list(tag_list)

    def serialize(self, obj: TagBase) -> Tuple[Any, ...]:
        return obj.serialize()

    def unserialize(self, obj: TagBase, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)