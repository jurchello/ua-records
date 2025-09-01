from __future__ import annotations
from gramps.gen.lib.srcmediatype import SourceMediaType
from repositories.gramps_type_repository import GrampsTypeRepository

class SourceMediaTypeRepository(GrampsTypeRepository):
    AUDIO = 1
    BOOK = 2
    CARD = 3
    CUSTOM = 0
    ELECTRONIC = 4
    FICHE = 5
    FILM = 6
    MAGAZINE = 7
    MANUSCRIPT = 8
    MAP = 9
    NEWSPAPER = 10
    PHOTO = 11
    TOMBSTONE = 12
    UNKNOWN = -1
    VIDEO = 13

    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)