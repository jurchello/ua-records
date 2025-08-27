from __future__ import annotations
from typing import Iterator, Optional, List, Any
from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Note

from repositories.basic_primary_object_repository import BasicPrimaryObjectRepository


class NoteRepository(BasicPrimaryObjectRepository):

    def get_by_handle(self, handle: str) -> Optional[Note]:
        return self.db.get_note_from_handle(handle)

    def add(self, note: Note, description: str = "Add note") -> str:
        with DbTxn(description, self.db) as trans:
            return self.db.add_note(note, trans)

    def commit(self, note: Note, description: str = "Update note") -> None:
        with DbTxn(description, self.db) as trans:
            self.db.commit_note(note, trans)

    def iter_all(self) -> Iterator[Note]:
        return self.db.iter_notes()

    def get_text(self, note: Note) -> str:
        return note.get()
    
    def get_format(self, note: Note) -> int:
        return note.get_format()
    
    def get_type(self, note: Note) -> str:
        return note.get_type()
    
    def get_styledtext(self, note: Note) -> Any:
        return note.get_styledtext()
    
    def append_text(self, note: Note, text: str) -> None:
        note.append(text)
    
    def set_text(self, note: Note, text: str) -> None:
        note.set(text)