from __future__ import annotations
from repositories.gramps_type_repository import GrampsTypeRepository

class NameOriginTypeRepository(GrampsTypeRepository):
    CUSTOM = 0
    FEUDAL = 7
    GIVEN = 3
    INHERITED = 2
    LOCATION = 12
    MATRILINEAL = 10
    MATRONYMIC = 6
    NONE = 1
    OCCUPATION = 11
    PATRILINEAL = 9
    PATRONYMIC = 5
    PSEUDONYM = 8
    TAKEN = 4
    UNKNOWN = -1

    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)