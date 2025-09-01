from __future__ import annotations
from gramps.gen.lib.familyreltype import FamilyRelType
from repositories.gramps_type_repository import GrampsTypeRepository

class FamilyRelTypeRepository(GrampsTypeRepository):
    CIVIL_UNION = 2
    CUSTOM = 4
    MARRIED = 0
    UNKNOWN = 3
    UNMARRIED = 1

    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)