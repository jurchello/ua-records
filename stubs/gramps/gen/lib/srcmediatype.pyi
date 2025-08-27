from .grampstype import GrampsType

class SourceMediaType(GrampsType):
    AUDIO = 0
    BOOK = 1
    CARD = 2
    ELECTRONIC = 3
    FICHE = 4
    FILM = 5
    MAGAZINE = 6
    MANUSCRIPT = 7
    MAP = 8
    NEWSPAPER = 9
    PHOTO = 10
    TOMBSTONE = 11
    VIDEO = 12
    UNKNOWN = 13

    def __init__(self, value: int | None = ...) -> None: ...