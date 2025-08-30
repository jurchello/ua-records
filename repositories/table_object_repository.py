from __future__ import annotations

from gramps.gen.lib import TableObject

from repositories.base_repository import BaseRepository


class TableObjectRepository(BaseRepository):

    def get_handle(self, obj: TableObject) -> str:
        return obj.get_handle()

    def get_change_time(self, obj: TableObject) -> int:
        return obj.get_change_time()

    def get_change_display(self, obj: TableObject) -> str:
        return obj.get_change_display()
