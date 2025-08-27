from __future__ import annotations
from typing import Any
from gramps.gen.lib import Date

from repositories.base_repository import BaseRepository


class DateRepository(BaseRepository):
    
    def get_text(self, date: Date) -> str:
        return date.get_text()
    
    def get_year(self, date: Date) -> int:
        return date.get_year()
    
    def get_month(self, date: Date) -> int:
        return date.get_month()
    
    def get_day(self, date: Date) -> int:
        return date.get_day()
    
    def get_modifier(self, date: Date) -> int:
        return date.get_modifier()
    
    def get_quality(self, date: Date) -> int:
        return date.get_quality()
    
    def get_calendar(self, date: Date) -> int:
        return date.get_calendar()
    
    def get_start_date(self, date: Date) -> tuple[int, int, int, Any]:
        return date.get_start_date()
    
    def get_stop_date(self, date: Date) -> tuple[int, int, int, Any]:
        return date.get_stop_date()