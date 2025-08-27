from __future__ import annotations
from typing import List
from gramps.gen.lib import CitationBase

from repositories.base_repository import BaseRepository


class CitationBaseRepository(BaseRepository):
    
    def get_citation_list(self, obj: CitationBase) -> List[str]:
        return obj.get_citation_list()