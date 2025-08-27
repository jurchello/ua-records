from .grampstype import GrampsType

class StyledTextTagType(GrampsType):
    BOLD = 0
    ITALIC = 1
    UNDERLINE = 2
    FONTCOLOR = 3
    HIGHLIGHT = 4
    FONTFACE = 5
    FONTSIZE = 6
    LINK = 7
    SUPERSCRIPT = 8

    def __init__(self, value: int | None = ...) -> None: ...