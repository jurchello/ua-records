from __future__ import annotations

from typing import Any, List

from gramps.gen.lib.citationbase import IndirectCitationBase

from repositories.repository_core import RepositoryCore


class IndirectCitationBaseRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_citation_child_list(self, obj) -> List[Any]:
        return obj.get_citation_child_list()

    def get_citation_list(self, obj) -> List[str]:
        return obj.get_citation_list()

    def has_citation_reference(self, obj, citation_handle: str) -> bool:
        return obj.has_citation_reference(citation_handle)

    def remove_citation_references(self, obj, citation_handle_list: List[str]) -> None:
        obj.remove_citation_references(citation_handle_list)

    def replace_citation_references(self, obj, old_handle: str, new_handle: str) -> None:
        obj.replace_citation_references(old_handle, new_handle)

    def citation_list(self, obj) -> List[str]:
        try:
            return obj.citation_list
        except AttributeError:
            return obj.get_citation_list()
