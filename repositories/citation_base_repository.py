from __future__ import annotations

from typing import Any, List, Tuple

from repositories.repository_core import RepositoryCore


class CitationBaseRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def add_citation(self, obj, handle: str) -> bool:
        return obj.add_citation(handle)

    def get_all_citation_lists(self, obj) -> List[str]:
        return obj.get_all_citation_lists()

    def get_citation_child_list(self, obj) -> List[Any]:
        return obj.get_citation_child_list()

    def get_citation_list(self, obj) -> List[str]:
        return obj.get_citation_list()

    def get_referenced_citation_handles(self, obj) -> List[Tuple[str, str]]:
        return obj.get_referenced_citation_handles()

    def has_citation_reference(self, obj, citation_handle: str) -> bool:
        return obj.has_citation_reference(citation_handle)

    def remove_citation_references(self, obj, citation_handle_list: List[str]) -> None:
        obj.remove_citation_references(citation_handle_list)

    def replace_citation_references(self, obj, old_handle: str, new_handle: str) -> None:
        obj.replace_citation_references(old_handle, new_handle)

    def serialize(self, obj) -> Tuple[Any, ...]:
        return obj.serialize()

    def set_citation_list(self, obj, citation_list: List[str]) -> None:
        obj.set_citation_list(citation_list)

    def unserialize(self, obj, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)
