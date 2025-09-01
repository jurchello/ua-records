from __future__ import annotations
from repositories.gramps_type_repository import GrampsTypeRepository

class MarkerTypeRepository(GrampsTypeRepository):
    COMPLETE = 1
    CUSTOM = 0
    NONE = -1
    TODO_TYPE = 2

    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)