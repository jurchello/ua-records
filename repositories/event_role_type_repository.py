from __future__ import annotations

from gramps.gen.lib import EventRoleType

from repositories.gramps_type_repository import GrampsTypeRepository


class EventRoleTypeRepository(GrampsTypeRepository):
    AIDE = 4
    BRIDE = 5
    CELEBRANT = 3
    CLERGY = 2
    CUSTOM = 0
    FAMILY = 8
    GROOM = 6
    INFORMANT = 9
    PRIMARY = 1
    UNKNOWN = -1
    WITNESS = 7
    GODPARENT_GRAMPS_6_0 = 10

    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def is_family(self, obj: EventRoleType) -> bool:
        return obj.is_family()

    def is_primary(self, obj: EventRoleType) -> bool:
        return obj.is_primary()

