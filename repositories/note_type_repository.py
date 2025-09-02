from __future__ import annotations
from typing import List
from gramps.gen.lib.notetype import NoteType
from repositories.gramps_type_repository import GrampsTypeRepository

class NoteTypeRepository(GrampsTypeRepository):
    ADDRESS = 6
    ASSOCIATION = 7
    ATTRIBUTE = 5
    CHILDREF = 19
    CITATION = 22
    CUSTOM = 0
    EVENT = 10
    EVENTREF = 11
    FAMILY = 9
    GENERAL = 1
    HTML_CODE = 24
    LDS = 8
    LINK = 26
    MEDIA = 17
    MEDIAREF = 18
    PERSON = 4
    PERSONNAME = 20
    PLACE = 14
    REPO = 15
    REPOREF = 16
    REPORT_TEXT = 23
    RESEARCH = 2
    SOURCE = 12
    SOURCEREF = 13
    SOURCE_TEXT = 21
    TODO = 25
    TRANSCRIPT = 3
    UNKNOWN = -1

    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def get_ignore_list(self, obj, exception: List[int]) -> List[int]:
        return obj.get_ignore_list(exception)