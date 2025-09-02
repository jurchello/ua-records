from __future__ import annotations
from typing import Any, List, Tuple
from gramps.gen.lib.src import Source
from repositories.media_base_repository import MediaBaseRepository
from repositories.note_base_repository import NoteBaseRepository
from repositories.src_attribute_base_repository import SrcAttributeBaseRepository
from repositories.indirect_citation_base_repository import IndirectCitationBaseRepository
from repositories.primary_object_repository import PrimaryObjectRepository

class SourceRepository(
    MediaBaseRepository,
    NoteBaseRepository,
    SrcAttributeBaseRepository,
    IndirectCitationBaseRepository,
    PrimaryObjectRepository,
):
    def __init__(self, db=None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def add_repo_reference(self, obj, repo_ref: Any) -> None:
        obj.add_repo_reference(repo_ref)

    def get_abbreviation(self, obj) -> str:
        return obj.get_abbreviation()

    def get_author(self, obj) -> str:
        return obj.get_author()

    def get_citation_child_list(self, obj) -> List[Any]:
        return obj.get_citation_child_list()

    def get_handle_referents(self, obj) -> List[Any]:
        return obj.get_handle_referents()

    def get_note_child_list(self, obj) -> List[Any]:
        return obj.get_note_child_list()

    def get_publication_info(self, obj) -> str:
        return obj.get_publication_info()

    def get_referenced_handles(self, obj) -> List[Tuple[str, str]]:
        return obj.get_referenced_handles()

    def get_reporef_list(self, obj) -> List[Any]:
        return obj.get_reporef_list()

    @classmethod
    def get_schema(cls) -> dict:
        return Source.get_schema()

    def get_text_data_child_list(self, obj) -> List[Any]:
        return obj.get_text_data_child_list()

    def get_text_data_list(self, obj) -> List[Any]:
        return obj.get_text_data_list()

    def get_title(self, obj) -> str:
        return obj.get_title()

    def has_repo_reference(self, obj, repo_handle: str) -> bool:
        return obj.has_repo_reference(repo_handle)

    def merge(self, obj, acquisition) -> None:
        obj.merge(acquisition)

    def remove_repo_references(self, obj, repo_handle_list: List[str]) -> None:
        obj.remove_repo_references(repo_handle_list)

    def replace_repo_references(self, obj, old_handle: str, new_handle: str) -> None:
        obj.replace_repo_references(old_handle, new_handle)

    def serialize(self, obj) -> Any:
        return obj.serialize()

    def set_abbreviation(self, obj, abbrev: str) -> None:
        obj.set_abbreviation(abbrev)

    def set_author(self, obj, author: str) -> None:
        obj.set_author(author)

    def set_publication_info(self, obj, text: str) -> None:
        obj.set_publication_info(text)

    def set_reporef_list(self, obj, reporef_list: List[Any]) -> None:
        obj.set_reporef_list(reporef_list)

    def set_title(self, obj, title: str) -> None:
        obj.set_title(title)

    def unserialize(self, obj, data: Any) -> None:
        obj.unserialize(data)

    def title(self, obj) -> str:
        try:
            return obj.title
        except AttributeError:
            return obj.get_title()

    def author(self, obj) -> str:
        try:
            return obj.author
        except AttributeError:
            return obj.get_author()

    def publication_info(self, obj) -> str:
        try:
            return obj.publication_info
        except AttributeError:
            return obj.get_publication_info()