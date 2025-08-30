from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass
class AfterGraph:
    """Simple holder for the target (After) JSON graph: {(kind, oid) -> payload}.
    HV-only (no selectors).
    """

    objects: Dict[Tuple[str, str], Dict[str, Any]] = field(default_factory=dict)

    def put(self, key, data: Dict[str, Any]) -> None:
        # key is ObjKey-like: has .kind and .oid
        self.objects[(key.kind, key.oid)] = data

    def get(self, key) -> Dict[str, Any] | None:
        return self.objects.get((key.kind, key.oid))

    def as_map(self) -> Dict[Tuple[str, str], Dict[str, Any]]:
        return dict(self.objects)
