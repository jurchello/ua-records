from __future__ import annotations
from typing import Iterator, Optional, List, Any
from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Source

from repositories.basic_primary_object_repository import BasicPrimaryObjectRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.citation_base_repository import CitationBaseRepository


class SourceRepository(BasicPrimaryObjectRepository, NoteBaseRepository, CitationBaseRepository):

    def get_by_handle(self, handle: str) -> Optional[Source]:
        return self.db.get_source_from_handle(handle)

    def add(self, source: Source, description: str = "Add source") -> str:
        with DbTxn(description, self.db) as trans:
            return self.db.add_source(source, trans)

    def commit(self, source: Source, description: str = "Update source") -> None:
        with DbTxn(description, self.db) as trans:
            self.db.commit_source(source, trans)

    def iter_all(self) -> Iterator[Source]:
        return self.db.iter_sources()

    def get_abbreviation(self, source: Source) -> str:
        return source.get_abbreviation()
    
    def get_author(self, source: Source) -> str:
        return source.get_author()
    
    def get_publication_info(self, source: Source) -> str:
        return source.get_publication_info()
    
    def get_title(self, source: Source) -> str:
        return source.get_title()
    
    def get_reporef_list(self, source: Source) -> List[Any]:
        return source.get_reporef_list()
    
    def has_repo_reference(self, source: Source, repo_handle: str) -> bool:
        return source.has_repo_reference(repo_handle)