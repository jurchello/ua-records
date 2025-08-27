from __future__ import annotations
from typing import Optional
from gramps.gen.lib import Span

from repositories.base_repository import BaseRepository


class SpanRepository(BaseRepository):
    
    def get_start_date(self, span: Span) -> Optional[tuple[int, int, int]]:
        return span.get_start_date()
    
    def get_end_date(self, span: Span) -> Optional[tuple[int, int, int]]:
        return span.get_end_date()
    
    def get_years_months_days(self, span: Span) -> tuple[int, int, int]:
        return span.get_years_months_days()
    
    def is_valid(self, span: Span) -> bool:
        return span.is_valid()