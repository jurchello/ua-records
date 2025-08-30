from __future__ import annotations

from dataclasses import dataclass

VH_PREFIX = "VH:"


@dataclass(frozen=True)
class ID:
    raw: str

    def is_virtual(self) -> bool:
        return self.raw.startswith(VH_PREFIX)

    def is_handle(self) -> bool:
        return not self.is_virtual()

    def __str__(self) -> str:
        return self.raw


def h(handle: str) -> ID:
    # Real Gramps handle (UUID). No prefix, use as-is.
    return ID(handle)


def vh(local: str) -> ID:
    return ID(local if local.startswith(VH_PREFIX) else VH_PREFIX + local)
