from __future__ import annotations

from typing import Iterator, Optional

from gramps.gen.db.txn import DbTxn
from gramps.gen.lib import Media

from repositories.attribute_base_repository import AttributeBaseRepository
from repositories.basic_primary_object_repository import BasicPrimaryObjectRepository
from repositories.citation_base_repository import CitationBaseRepository
from repositories.date_base_repository import DateBaseRepository
from repositories.note_base_repository import NoteBaseRepository


class MediaRepository(
    BasicPrimaryObjectRepository,
    NoteBaseRepository,
    CitationBaseRepository,
    AttributeBaseRepository,
    DateBaseRepository,
):

    def get_by_handle(self, handle: str) -> Optional[Media]:
        return self.db.get_media_from_handle(handle)

    def add(self, media: Media, description: str = "Add media") -> str:
        with DbTxn(description, self.db) as trans:
            return self.db.add_media(media, trans)

    def commit(self, media: Media, description: str = "Update media") -> None:
        with DbTxn(description, self.db) as trans:
            self.db.commit_media(media, trans)

    def iter_all(self) -> Iterator[Media]:
        return self.db.iter_media()

    def get_path(self, media: Media) -> str:
        return media.get_path()

    def get_mime_type(self, media: Media) -> str:
        return media.get_mime_type()

    def get_description(self, media: Media) -> str:
        return media.get_description()

    def get_checksum(self, media: Media) -> str:
        return media.get_checksum()
