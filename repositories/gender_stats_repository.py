from __future__ import annotations

from typing import Any

from gramps.gen.lib import GenderStats

from repositories.repository_core import RepositoryCore


class GenderStatsRepository(RepositoryCore):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)

    def clear_stats(self, obj: GenderStats) -> None:
        obj.clear_stats()

    def count_name(self, obj: GenderStats, name: str, gender: int) -> None:
        obj.count_name(name, gender)

    def count_person(self, obj: GenderStats, person: Any, undo: int = 0) -> None:
        obj.count_person(person, undo=undo)

    def guess_gender(self, obj: GenderStats, name: str) -> Any:
        return obj.guess_gender(name)

    def name_stats(self, obj: GenderStats, name: str) -> Any:
        return obj.name_stats(name)

    def save_stats(self, obj: GenderStats) -> None:
        obj.save_stats()

    def uncount_person(self, obj: GenderStats, person: Any) -> None:
        obj.uncount_person(person)
