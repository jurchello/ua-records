from __future__ import annotations

from typing import Any

from gramps.gen.lib import Surname

from repositories.base_repository import BaseRepository


class SurnameRepository(BaseRepository):

    def get_surname(self, surname: Surname) -> str:
        return surname.get_surname()

    def get_type(self, surname: Surname) -> Any:
        return surname.get_type()
