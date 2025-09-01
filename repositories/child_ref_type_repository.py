from __future__ import annotations
from repositories.gramps_type_repository import GrampsTypeRepository

class ChildRefTypeRepository(GrampsTypeRepository):
    ADOPTED = 2
    BIRTH = 1
    CUSTOM = 7
    FOSTER = 5
    NONE = 0
    SPONSORED = 4
    STEPCHILD = 3
    UNKNOWN = 6

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)
