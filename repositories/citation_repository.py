from __future__ import annotations
from typing import Optional

from gramps.gen.db.txn import DbTxn
from gramps.gen.lib.citation import Citation

from repositories.base_repository import BaseRepository


class CitationRepository(BaseRepository):
    def get_by_handle(self, handle: str) -> Optional[Citation]:
        return self.db.get_citation_from_handle(handle)

    def add(self, citation: Citation, description: str = "Add citation") -> str:
        with DbTxn(description, self.db) as trans:
            return self.db.add_citation(citation, trans)

    def commit(self, citation: Citation, description: str = "Update citation") -> None:
        with DbTxn(description, self.db) as trans:
            self.db.commit_citation(citation, trans)