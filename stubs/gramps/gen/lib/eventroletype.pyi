from .grampstype import GrampsType

class EventRoleType(GrampsType):
    CUSTOM = 0
    PRIMARY = 1
    CLERGY = 2
    CELEBRANT = 3
    AIDE = 4
    BRIDE = 5
    GROOM = 6
    WITNESS = 7
    FAMILY = 8
    INFORMANT = 9
    UNKNOWN = -1

    def is_family(self) -> bool: ...
    def is_primary(self) -> bool: ...