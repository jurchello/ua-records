from __future__ import annotations
from typing import Iterator, Optional
from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Person

from repositories.base_repository import BaseRepository


class PersonRepository(BaseRepository):
    
    def get_by_handle(self, handle: str) -> Optional[Person]:
        return self.db.get_person_from_handle(handle)

    def add(self, person: Person, description: str = "Add person") -> str:
        with DbTxn(description, self.db) as trans:
            return self.db.add_person(person, trans)
    
    def commit(self, person: Person, description: str = "Update person") -> None:
        with DbTxn(description, self.db) as trans:
            self.db.commit_person(person, trans)
    
    def iter_all(self) -> Iterator[Person]:
        return self.db.iter_people()