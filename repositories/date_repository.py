from __future__ import annotations

from typing import Any, Literal, Optional, Tuple, Union

from gramps.gen.lib import Date

from repositories.repository_core import RepositoryCore


class DateRepository(RepositoryCore):

    CALENDARS = range(0, 7)
    CAL_FRENCH = 3
    CAL_GREGORIAN = 0
    CAL_HEBREW = 2
    CAL_ISLAMIC = 5
    CAL_JULIAN = 1
    CAL_PERSIAN = 4
    CAL_SWEDISH = 6
    EMPTY = (0, 0, 0, False)
    MOD_ABOUT = 3
    MOD_AFTER = 2
    MOD_BEFORE = 1
    MOD_NONE = 0
    MOD_RANGE = 4
    MOD_SPAN = 5
    MOD_TEXTONLY = 6
    NEWYEAR_JAN1 = 0
    NEWYEAR_MAR1 = 1
    NEWYEAR_MAR25 = 2
    NEWYEAR_SEP1 = 3
    QUAL_CALCULATED = 2
    QUAL_ESTIMATED = 1
    QUAL_NONE = 0
    calendar_names = ["Gregorian", "Julian", "Hebrew", "French Republican", "Persian", "Islamic", "Swedish"]
    ui_calendar_names = ["Gregorian", "Julian", "Hebrew", "French Republican", "Persian", "Islamic", "Swedish"]

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def convert_calendar(self, obj: Date, calendar: int, known_valid: bool = True) -> None:
        obj.convert_calendar(calendar, known_valid=known_valid)

    def copy(self, obj: Date, source: Date) -> None:
        obj.copy(source)

    def copy_offset_ymd(self, obj: Date, year: int = 0, month: int = 0, day: int = 0) -> Date:
        return obj.copy_offset_ymd(year=year, month=month, day=day)

    def copy_ymd(self, obj: Date, year: int = 0, month: int = 0, day: int = 0, remove_stop_date: Optional[bool] = None) -> Date:
        return obj.copy_ymd(year=year, month=month, day=day, remove_stop_date=remove_stop_date)

    def get_calendar(self, obj: Date) -> int:
        return obj.get_calendar()

    def get_day(self, obj: Date) -> int:
        return obj.get_day()

    def get_day_valid(self, obj: Date) -> bool:
        return obj.get_day_valid()

    def get_dmy(self, obj: Date, get_slash: bool = False) -> Tuple[Any, ...]:
        return obj.get_dmy(get_slash=get_slash)

    def get_dow(self, obj: Date) -> Optional[int]:
        return obj.get_dow()

    def get_high_year(self, obj: Date) -> Optional[int]:
        return obj.get_high_year()

    def get_modifier(self, obj: Date) -> int:
        return obj.get_modifier()

    def get_month(self, obj: Date) -> int:
        return obj.get_month()

    def get_month_valid(self, obj: Date) -> bool:
        return obj.get_month_valid()

    def get_new_year(self, obj: Date) -> int:
        return obj.get_new_year()

    def get_quality(self, obj: Date) -> int:
        return obj.get_quality()

    def get_slash(self, obj: Date) -> bool:
        return obj.get_slash()

    def get_slash2(self, obj: Date) -> bool:
        return obj.get_slash2()

    def get_sort_value(self, obj: Date) -> int:
        return obj.get_sort_value()

    def get_start_date(self, obj: Date) -> Tuple[Any, ...]:
        return obj.get_start_date()

    def get_start_stop_range(self, obj: Date) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
        return obj.get_start_stop_range()

    def get_stop_date(self, obj: Date) -> Tuple[Any, ...]:
        return obj.get_stop_date()

    def get_stop_day(self, obj: Date) -> int:
        return obj.get_stop_day()

    def get_stop_month(self, obj: Date) -> int:
        return obj.get_stop_month()

    def get_stop_year(self, obj: Date) -> int:
        return obj.get_stop_year()

    def get_stop_ymd(self, obj: Date) -> Tuple[int, int, int]:
        return obj.get_stop_ymd()

    def get_text(self, obj: Date) -> str:
        return obj.get_text()

    def get_valid(self, obj: Date) -> bool:
        return obj.get_valid()

    def get_year(self, obj: Date) -> int:
        return obj.get_year()

    def get_year_calendar(self, obj: Date, calendar_name: Optional[str] = None) -> int:
        return obj.get_year_calendar(calendar_name=calendar_name)

    def get_year_valid(self, obj: Date) -> bool:
        return obj.get_year_valid()

    def get_ymd(self, obj: Date) -> Tuple[int, int, int]:
        return obj.get_ymd()

    def is_compound(self, obj: Date) -> bool:
        return obj.is_compound()

    def is_empty(self, obj: Date) -> bool:
        return obj.is_empty()

    def is_equal(self, obj: Date, other: Date) -> bool:
        return bool(obj.is_equal(other))

    def is_full(self, obj: Date) -> bool:
        return obj.is_full()

    def is_regular(self, obj: Date) -> bool:
        return obj.is_regular()

    def is_valid(self, obj: Date) -> bool:
        return obj.is_valid()

    def lookup_calendar(self, obj: Date, calendar: Any) -> int:
        return obj.lookup_calendar(calendar)

    def lookup_modifier(self, obj: Date, modifier: Any) -> int:
        return obj.lookup_modifier(modifier)

    def lookup_quality(self, obj: Date, quality: Any) -> int:
        return obj.lookup_quality(quality)

    def make_vague(self, obj: Date) -> None:
        obj.make_vague()

    def match(self, obj: Date, other_date: Date, comparison: str = "=") -> bool:
        return obj.match(other_date, comparison=comparison)

    def match_exact(self, obj: Date, other_date: Date) -> bool:
        return obj.match_exact(other_date)

    @staticmethod
    def newyear_to_code(string: str) -> Union[tuple[int, ...], Literal[0, 1, 2, 3]]:
        return Date.newyear_to_code(string)

    def newyear_to_str(self, obj: Date) -> str:
        return obj.newyear_to_str()

    def offset(self, obj: Date, value: int) -> Tuple[int, int, int]:
        return obj.offset(value)

    def offset_date(self, obj: Date, value: int) -> Date:
        return obj.offset_date(value)

    def recalc_sort_value(self, obj: Date) -> int:
        return obj.recalc_sort_value()

    def serialize(self, obj: Date, no_text_date: bool = False) -> Any:
        return obj.serialize(no_text_date=no_text_date)

    def set(self, obj: Date, quality: Optional[int] = None, modifier: Optional[int] = None, calendar: Optional[int] = None, value: Optional[Tuple[Any, ...]] = None, text: Optional[str] = None, newyear: Any = 0) -> None:
        obj.set(quality=quality, modifier=modifier, calendar=calendar, value=value, text=text, newyear=newyear)

    def set2_yr_mon_day(self, obj: Date, year: int, month: int, day: int) -> None:
        obj.set2_yr_mon_day(year, month, day)

    def set2_yr_mon_day_offset(self, obj: Date, year: int = 0, month: int = 0, day: int = 0) -> None:
        obj.set2_yr_mon_day_offset(year=year, month=month, day=day)

    def set_as_text(self, obj: Date, text: str) -> None:
        obj.set_as_text(text)

    def set_calendar(self, obj: Date, val: int) -> None:
        obj.set_calendar(val)

    def set_modifier(self, obj: Date, val: int) -> None:
        obj.set_modifier(val)

    def set_new_year(self, obj: Date, value: Any) -> None:
        obj.set_new_year(value)

    def set_quality(self, obj: Date, val: int) -> None:
        obj.set_quality(val)

    def set_slash(self, obj: Date, value: int) -> None:
        obj.set_slash(value)

    def set_slash2(self, obj: Date, value: int) -> None:
        obj.set_slash2(value)

    def set_text_value(self, obj: Date, text: str) -> None:
        obj.set_text_value(text)

    def set_year(self, obj: Date, year: int) -> None:
        obj.set_year(year)

    def set_yr_mon_day(self, obj: Date, year: int, month: int, day: int, remove_stop_date: Optional[bool] = None) -> None:
        obj.set_yr_mon_day(year, month, day, remove_stop_date=remove_stop_date)

    def set_yr_mon_day_offset(self, obj: Date, year: int = 0, month: int = 0, day: int = 0) -> None:
        obj.set_yr_mon_day_offset(year=year, month=month, day=day)

    def to_calendar(self, obj: Date, calendar_name: str) -> Date:
        return obj.to_calendar(calendar_name)

    @classmethod
    def get_schema(cls) -> dict:
        return Date.get_schema()

    def unserialize(self, obj: Date, data: Any) -> None:
        obj.unserialize(data)

    def year(self, obj: Date) -> int:
        try:
            return obj.year
        except AttributeError:
            return obj.get_year()


