from __future__ import annotations
from gramps.gen.lib import DateBase, Date

from repositories.base_repository import BaseRepository


class DateBaseRepository(BaseRepository):
    
    def get_date_object(self, obj: DateBase) -> Date:
        return obj.get_date_object()