from __future__ import annotations
from typing import Iterator, Optional, List, Any
from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Repository

from repositories.basic_primary_object_repository import BasicPrimaryObjectRepository
from repositories.note_base_repository import NoteBaseRepository


class RepositoryRepository(BasicPrimaryObjectRepository, NoteBaseRepository):

    def get_by_handle(self, handle: str) -> Optional[Repository]:
        return self.db.get_repository_from_handle(handle)

    def add(self, repository: Repository, description: str = "Add repository") -> str:
        with DbTxn(description, self.db) as trans:
            return self.db.add_repository(repository, trans)

    def commit(self, repository: Repository, description: str = "Update repository") -> None:
        with DbTxn(description, self.db) as trans:
            self.db.commit_repository(repository, trans)

    def iter_all(self) -> Iterator[Repository]:
        return self.db.iter_repositories()

    def get_name(self, repository: Repository) -> str:
        return repository.get_name()
    
    def get_type(self, repository: Repository) -> Any:
        return repository.get_type()