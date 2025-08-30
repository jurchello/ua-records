from __future__ import annotations

from gramps.gen.lib import MediaRef

from repositories.base_repository import BaseRepository


class MediaRefRepository(BaseRepository):

    def get_reference_handle(self, media_ref: MediaRef) -> str:
        return media_ref.get_reference_handle()

    def get_rectangle(self, media_ref: MediaRef) -> tuple[int, int, int, int]:
        return media_ref.get_rectangle()

    def is_equivalent(self, media_ref: MediaRef, other: MediaRef) -> bool:
        return media_ref.is_equivalent(other)
