from __future__ import annotations
from typing import Any, List, Tuple, Union
from gramps.gen.lib.note import Note
from gramps.gen.lib.styledtext import StyledText
from gramps.gen.lib.notetype import NoteType
from repositories.basic_primary_object_repository import BasicPrimaryObjectRepository

class NoteRepository(BasicPrimaryObjectRepository):
    FLOWED = 0
    FORMATTED = 1
    POS_CHANGE = 5
    POS_FORMAT = 3
    POS_HANDLE = 0
    POS_ID = 1
    POS_PRIVATE = 7
    POS_TAGS = 6
    POS_TEXT = 2
    POS_TYPE = 4

    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def append(self, obj: Note, text: Any) -> None:
        obj.append(text)

    def get(self, obj: Note) -> str:
        return obj.get()

    def get_format(self, obj: Note) -> int:
        return obj.get_format()

    def get_links(self, obj: Note) -> List[Tuple[str, str, str, str]]:
        return obj.get_links()

    def get_referenced_handles(self, obj: Note) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    @classmethod
    def get_schema(cls) -> dict:
        return Note.get_schema()

    def get_styledtext(self, obj: Note) -> Any:
        return obj.get_styledtext()

    def get_text_data_list(self, obj: Note) -> List[Any]:
        return obj.get_text_data_list()

    def get_type(self, obj: Note) -> NoteType:
        return obj.get_type()
    
    def merge(self, obj: Note, acquisition: Note) -> None:
        obj.merge(acquisition)

    def serialize(self, obj: Note) -> Tuple[Any, ...]:
        return obj.serialize()

    def set(self, obj: Note, text: str) -> None:
        obj.set(text)

    def set_format(self, obj: Note, format: int) -> None:
        obj.set_format(format)

    def set_styledtext(self, obj: Note, text: Any) -> None:
        obj.set_styledtext(text)

    def set_type(self, obj: Note, the_type: str) -> None:
        obj.set_type(the_type)

    def unserialize(self, obj: Note, data: Tuple[Any, ...]) -> None:
        obj.unserialize(data)
        
    def text(self, obj: Note) -> Union[str, StyledText]:
        try:
            return obj.text
        except AttributeError:
            return obj.get()