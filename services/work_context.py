from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gramps.gen.db import DbReadBase
    from services.form_state_base import FormStateBase


@dataclass
class WorkContext:
    form_state: FormStateBase | None = None
    db: DbReadBase | None = None

    def reset(self) -> None:
        self.form_state = None
        self.db = None
