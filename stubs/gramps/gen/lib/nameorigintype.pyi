from .grampstype import GrampsType

class NameOriginType(GrampsType):
    CUSTOM = 0
    NONE = 1
    INHERITED = 2
    GIVEN = 3
    TAKEN = 4
    PATRONYMIC = 5
    MATRONYMIC = 6
    FEUDAL = 7
    PSEUDONYM = 8
    PATRILINEAL = 9
    MATRILINEAL = 10
    OCCUPATION = 11
    LOCATION = 12
    UNKNOWN = -1