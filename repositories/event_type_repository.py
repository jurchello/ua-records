from __future__ import annotations
from typing import Callable
from gramps.gen.lib.eventtype import EventType
from repositories.gramps_type_repository import GrampsTypeRepository

class EventTypeRepository(GrampsTypeRepository):
    ADOPT = 11
    ADULT_CHRISTEN = 14
    ANNULMENT = 9
    BAPTISM = 15
    BAR_MITZVAH = 16
    BAS_MITZVAH = 17
    BIRTH = 12
    BLESS = 18
    BURIAL = 19
    CAUSE_DEATH = 20
    CENSUS = 21
    CHRISTEN = 22
    CONFIRMATION = 23
    CREMATION = 24
    CUSTOM = 0
    DEATH = 13
    DEGREE = 25
    DIVORCE = 7
    DIV_FILING = 8
    EDUCATION = 26
    ELECTED = 27
    EMIGRATION = 28
    ENGAGEMENT = 6
    FIRST_COMMUN = 29
    GRADUATION = 31
    IMMIGRATION = 30
    MARRIAGE = 1
    MARR_ALT = 10
    MARR_BANNS = 5
    MARR_CONTR = 4
    MARR_LIC = 3
    MARR_SETTL = 2
    MED_INFO = 32
    MILITARY_SERV = 33
    NATURALIZATION = 34
    NOB_TITLE = 35
    NUM_MARRIAGES = 36
    OCCUPATION = 37
    ORDINATION = 38
    PROBATE = 39
    PROPERTY = 40
    RELIGION = 41
    RESIDENCE = 42
    RETIREMENT = 43
    UNKNOWN = -1
    WILL = 44

    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_abbreviation(self, obj: EventType, trans_text: Callable[[str], str] | None = None) -> str:
        return obj.get_abbreviation(trans_text=trans_text)

    def is_baptism(self, obj: EventType) -> bool:
        return obj.is_baptism()

    def is_birth(self, obj: EventType) -> bool:
        return obj.is_birth()

    def is_birth_fallback(self, obj: EventType) -> bool:
        return obj.is_birth_fallback()

    def is_burial(self, obj: EventType) -> bool:
        return obj.is_burial()

    def is_death(self, obj: EventType) -> bool:
        return obj.is_death()

    def is_death_fallback(self, obj: EventType) -> bool:
        return obj.is_death_fallback()

    def is_divorce(self, obj: EventType) -> bool:
        return obj.is_divorce()

    def is_divorce_fallback(self, obj: EventType) -> bool:
        return obj.is_divorce_fallback()

    def is_marriage(self, obj: EventType) -> bool:
        return obj.is_marriage()

    def is_marriage_fallback(self, obj: EventType) -> bool:
        return obj.is_marriage_fallback()

    def is_relationship_event(self, obj: EventType) -> bool:
        return obj.is_relationship_event()

    def is_type(self, obj: EventType, event_name: str) -> bool:
        return obj.is_type(event_name)