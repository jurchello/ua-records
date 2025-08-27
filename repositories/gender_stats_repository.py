from __future__ import annotations
from typing import Tuple, Any
from gramps.gen.lib import GenderStats

from repositories.base_repository import BaseRepository


class GenderStatsRepository(BaseRepository):
    """Repository for GenderStats objects with all GenderStats-specific methods."""

    # GenderStats-specific methods from stub
    def count_person(self, stats: GenderStats, person: Any, db: Any, date: Any | None = None) -> None:
        """Count a person in the gender statistics."""
        stats.count_person(person, db, date)

    def get_female_count(self, stats: GenderStats) -> int:
        """Return the count of females."""
        return stats.get_female_count()

    def get_male_count(self, stats: GenderStats) -> int:
        """Return the count of males."""
        return stats.get_male_count()

    def get_stats(self, stats: GenderStats) -> Tuple[int, int, int]:
        """Return the statistics as (male_count, female_count, unknown_count)."""
        return stats.get_stats()

    def get_unknown_count(self, stats: GenderStats) -> int:
        """Return the count of unknown gender."""
        return stats.get_unknown_count()