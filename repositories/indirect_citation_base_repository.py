from __future__ import annotations

from typing import Any, List

from gramps.gen.lib.citationbase import IndirectCitationBase

from repositories.base_repository import BaseRepository


class IndirectCitationBaseRepository(BaseRepository):
    """Repository for IndirectCitationBase objects with all IndirectCitationBase-specific methods."""

    # IndirectCitationBase-specific methods from stub
    def get_citation_child_list(self, indirect_citation_base: IndirectCitationBase) -> List[Any]:
        """Return the list of child secondary objects that may refer citations."""
        return indirect_citation_base.get_citation_child_list()

    def get_citation_list(self, indirect_citation_base: IndirectCitationBase) -> List[str]:
        """Return the list of Citation handles referenced by the object."""
        return indirect_citation_base.get_citation_list()

    def has_citation_reference(self, indirect_citation_base: IndirectCitationBase, citation_handle: str) -> bool:
        """Return True if the object has a reference to the given Citation handle."""
        return indirect_citation_base.has_citation_reference(citation_handle)

    def remove_citation_references(
        self, indirect_citation_base: IndirectCitationBase, citation_handle_list: List[str]
    ) -> None:
        """Remove all references to the Citation handles in the list."""
        indirect_citation_base.remove_citation_references(citation_handle_list)

    def replace_citation_references(
        self, indirect_citation_base: IndirectCitationBase, old_handle: str, new_handle: str
    ) -> None:
        """Replace all references to old Citation handle with new Citation handle."""
        indirect_citation_base.replace_citation_references(old_handle, new_handle)
