from .grampstype import GrampsType

class UrlType(GrampsType):
    CUSTOM = 0
    EMAIL = 1
    WEB_HOME = 2
    WEB_SEARCH = 3
    WEB_FTP = 4
    UNKNOWN = 5

    def __init__(self, value: int | None = ...) -> None: ...