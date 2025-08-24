from .grampstype import GrampsType

class NoteType(GrampsType):
    CUSTOM = 0
    GENERAL = 1
    RESEARCH = 2
    TRANSCRIPT = 3
    PERSON = 4
    ATTRIBUTE = 5
    ADDRESS = 6
    ASSOCIATION = 7
    LDS = 8
    FAMILY = 9
    EVENT = 10
    EVENTREF = 11
    SOURCE = 12
    SOURCEREF = 13
    PLACE = 14
    REPO = 15
    REPOREF = 16
    MEDIA = 17
    MEDIAREF = 18
    CHILDREF = 19
    PERSONNAME = 20
    SOURCE_TEXT = 21
    CITATION = 22
    REPORT_TEXT = 23
    HTML_CODE = 24
    TODO = 25
    LINK = 26
    UNKNOWN = -1

    def get_ignore_list(self, exception: list[int]) -> list[int]: ...