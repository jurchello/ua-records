from .grampstype import GrampsType

class RepositoryType(GrampsType):
    LIBRARY = 0
    CEMTERY = 1
    CHURCH = 2
    ARCHIVE = 3
    ALBUM = 4
    WEB_SITE = 5
    BOOKSTORE = 6
    COLLECTION = 7
    SAFE = 8
    UNKNOWN = 9

    def __init__(self, value: int | None = ...) -> None: ...