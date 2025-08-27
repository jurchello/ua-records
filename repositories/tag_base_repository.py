from __future__ import annotations
from typing import List
from gramps.gen.lib import TagBase

from repositories.base_repository import BaseRepository


class TagBaseRepository(BaseRepository):
    
    def get_tag_list(self, obj: TagBase) -> List[str]:
        return obj.get_tag_list()