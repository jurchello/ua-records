from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from identity.identity_map import IdentityMap

if TYPE_CHECKING:
    from gramps.gen.db import DbReadBase
    from services.form_state_base import FormStateBase
    

@dataclass
class WorkContext:
    form_state: FormStateBase | None = None
    db: DbReadBase | None = None
    identity_map: IdentityMap = field(default_factory=IdentityMap)

    def reset(self) -> None:
        self.form_state = None
        self.db = None
        self.identity_map = IdentityMap()