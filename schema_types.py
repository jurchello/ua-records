from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

ID_KEYS: Tuple[str, ...] = ("handle", "id", "gid")

@dataclass(frozen=True)
class ObjKey:
    kind: str       # e.g., "Person", "Event", "Family"
    oid: str        # H: real UUID string from Gramps, or VH:* virtual id

    def is_virtual(self) -> bool:
        return self.oid.startswith("VH:")

    def is_handle(self) -> bool:
        return not self.is_virtual()

    def __str__(self) -> str:
        return f"{self.kind}:{self.oid}"