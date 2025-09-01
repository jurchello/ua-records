from __future__ import annotations
from repositories.gramps_type_repository import GrampsTypeRepository

class NameTypeRepository(GrampsTypeRepository):
    AKA = 1
    BIRTH = 2
    CUSTOM = 0
    MARRIED = 3
    UNKNOWN = -1

    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)