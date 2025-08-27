from __future__ import annotations
from typing import List
from gramps.gen.lib import NoteBase

from repositories.base_repository import BaseRepository


class NoteBaseRepository(BaseRepository):
    
    def get_note_list(self, obj: NoteBase) -> List[str]:
        return obj.get_note_list()