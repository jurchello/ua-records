from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Protocol for objects with gramps_id
    from typing import Protocol

    from form_state_base import FormStateBase

    class HasGrampsId(Protocol):
        def get_gramps_id(self) -> str: ...


class IdCollector:
    @staticmethod
    def collect(data: dict | list | tuple | set | str | int | None) -> set[str]:
        out: set[str] = set()
        IdCollector._walk(data, out)
        return out

    @staticmethod
    def collect_from_state(state: "FormStateBase | dict | list | tuple | set | None") -> set[str]:
        try:
            if hasattr(state, "to_dict") and callable(getattr(state, "to_dict")):
                return IdCollector.collect(state.to_dict())
        except Exception:
            pass
        return IdCollector.collect(state)  # type: ignore[arg-type]

    @staticmethod
    def to_text(ids: Iterable[str], sep: str = "$|^") -> str:
        cleaned = [s.strip() for s in ids if isinstance(s, str) and s.strip()]
        return sep.join(sorted(set(cleaned)))

    @staticmethod
    def _walk(node: dict | list | tuple | set | str | int | None, out: set[str]) -> None:
        if isinstance(node, dict):
            if "object" in node:
                IdCollector._maybe_add_from_object(node.get("object"), out)
            if "gramps_id" in node:
                IdCollector._maybe_add_from_value(node.get("gramps_id"), out)
            for v in node.values():
                IdCollector._walk(v, out)
            return

        if isinstance(node, (list, tuple, set)):
            for item in node:
                IdCollector._walk(item, out)
            return

        IdCollector._maybe_add_from_object(node, out)

    @staticmethod
    def _maybe_add_from_object(obj: "HasGrampsId | None", out: set[str]) -> None:
        if obj is None:
            return
        try:
            if hasattr(obj, "get_gramps_id"):
                gid = obj.get_gramps_id()
                IdCollector._maybe_add_from_value(gid, out)
        except Exception:
            pass

    @staticmethod
    def _maybe_add_from_value(value: object, out: set[str]) -> None:
        if value is None:
            return
        try:
            s = str(value).strip()
            if s:
                out.add(s)
        except Exception:
            pass
