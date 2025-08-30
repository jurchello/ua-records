from __future__ import annotations

from gramps.gen.lib import PrivacyBase

from repositories.base_repository import BaseRepository


class PrivacyBaseRepository(BaseRepository):

    def get_privacy(self, obj: PrivacyBase) -> bool:
        return obj.get_privacy()

    def set_privacy(self, obj: PrivacyBase, val: bool) -> None:
        obj.set_privacy(val)
