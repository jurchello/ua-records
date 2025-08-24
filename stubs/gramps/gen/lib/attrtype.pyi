from .grampstype import GrampsType

class AttributeType(GrampsType):
    CUSTOM = 0
    CASTE = 1
    DESCRIPTION = 2
    ID = 3
    NATIONAL = 4
    NUM_CHILD = 5
    SSN = 6
    NICKNAME = 7
    CAUSE = 8
    AGENCY = 9
    AGE = 10
    FATHER_AGE = 11
    MOTHER_AGE = 12
    WITNESS = 13
    TIME = 14
    OCCUPATION = 15
    UNKNOWN = -1

    def type2base(self) -> str: ...