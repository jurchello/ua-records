from .grampstype import GrampsType

class ChildRefType(GrampsType):
    NONE = 0
    BIRTH = 1
    ADOPTED = 2
    STEPCHILD = 3
    SPONSORED = 4
    FOSTER = 5
    UNKNOWN = 6
    CUSTOM = 7