from __future__ import annotations
from typing import Iterator, Optional, List, Any, Tuple
from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Citation

from repositories.base_repository import BaseRepository


class CitationRepository(BaseRepository):
    """Repository for Citation objects with full CRUD operations and all Citation-specific methods."""

    # CRUD Operations
    def get_by_handle(self, handle: str) -> Optional[Citation]:
        """Get Citation by handle from database."""
        return self.db.get_citation_from_handle(handle)

    def add(self, citation: Citation, description: str = "Add citation") -> str:
        """Add new Citation to database."""
        with DbTxn(description, self.db) as trans:
            return self.db.add_citation(citation, trans)

    def commit(self, citation: Citation, description: str = "Update citation") -> None:
        """Commit Citation changes to database."""
        with DbTxn(description, self.db) as trans:
            self.db.commit_citation(citation, trans)

    def iter_all(self) -> Iterator[Citation]:
        """Iterate over all Citations in database."""
        return self.db.iter_citations()

    # Citation-specific methods from stub
    def get_citation_child_list(self, citation: Citation) -> List[Any]:
        """Return the list of child secondary objects that may refer citations."""
        return citation.get_citation_child_list()

    def get_confidence_level(self, citation: Citation) -> int:
        """Return the confidence level of the Citation."""
        return citation.get_confidence_level()

    def get_handle_referents(self, citation: Citation) -> List[Any]:
        """Return the list of child objects which may reference primary objects."""
        return citation.get_handle_referents()

    def get_note_child_list(self, citation: Citation) -> List[Any]:
        """Return the list of child secondary objects that may refer notes."""
        return citation.get_note_child_list()

    def get_page(self, citation: Citation) -> str:
        """Return the page of the Citation."""
        return citation.get_page()

    def get_reference_handle(self, citation: Citation) -> str:
        """Return the reference handle of the Citation."""
        return citation.get_reference_handle()

    def get_referenced_handles(self, citation: Citation) -> List[Tuple[str, str]]:
        """Return the list of (classname, handle) tuples for all directly referenced primary objects."""
        return citation.get_referenced_handles()

    def get_text_data_child_list(self, citation: Citation) -> List[Any]:
        """Return the list of child objects that may carry textual data."""
        return citation.get_text_data_child_list()

    def get_text_data_list(self, citation: Citation) -> List[str]:
        """Return the list of all textual attributes of the object."""
        return citation.get_text_data_list()

    def merge(self, citation: Citation, acquisition: Citation) -> None:
        """Merge the content of acquisition into this citation."""
        citation.merge(acquisition)

    def serialize(self, citation: Citation, no_text_date: bool = False) -> Tuple[Any, ...]:
        """Convert the data held in the Citation to a Python tuple."""
        return citation.serialize(no_text_date)

    def set_confidence_level(self, citation: Citation, val: int) -> None:
        """Set the confidence level of the Citation."""
        citation.set_confidence_level(val)

    def set_page(self, citation: Citation, page: str) -> None:
        """Set the page of the Citation."""
        citation.set_page(page)

    def set_reference_handle(self, citation: Citation, val: str) -> None:
        """Set the reference handle of the Citation."""
        citation.set_reference_handle(val)

    def unserialize(self, citation: Citation, data: Tuple[Any, ...]) -> None:
        """Convert the data held in a tuple back into the data in a Citation object."""
        citation.unserialize(data)