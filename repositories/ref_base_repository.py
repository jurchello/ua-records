from __future__ import annotations

from typing import List, Tuple

from gramps.gen.lib import RefBase

from repositories.base_repository import BaseRepository


class RefBaseRepository(BaseRepository):

    def get_reference_handle(self, ref: RefBase) -> str:
        return ref.get_reference_handle()

    def set_reference_handle(self, ref: RefBase, handle: str) -> None:
        ref.set_reference_handle(handle)

    def get_referenced_handles(self, ref: RefBase) -> List[Tuple[str, str]]:
        return ref.get_referenced_handles()
